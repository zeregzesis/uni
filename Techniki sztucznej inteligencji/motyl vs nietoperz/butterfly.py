import argparse
from random import choice, randint, uniform
from numpy import exp, inf
from multiprocessing import Pool

from test_functions import f2, rastrigin, zakharov


class Butterfly:

    def __init__(self, dim, min, max, fitness):
        self.pos = [uniform(min, max) for _ in range(dim)]
        self.fitness = fitness
        self.fragrance = 0
        self.min = min
        self.max = max

    def bound(self):
        for i in range(len(self.pos)):
            if self.pos[i] < self.min:
                self.pos[i] = self.min
            elif self.pos[i] > self.max:
                self.pos[i] = self.max
    
    def updateFragrance(self, modal, modalExp, expected):
        self.fragrance = modal * (intensity(expected, self.fitness(self.pos), abs(self.max)) **modalExp)

    def globalSearch(self, currentBest):
        for dim in range(len(self.pos)):
            self.pos[dim] += ((uniform(0,1) **2 * currentBest.pos[dim] - self.pos[dim]) * self.fragrance)

    def localSearch(self, b1, b2):
        for dim in range(len(self.pos)):
            self.pos[dim] += ((uniform(0,1) **2 * b1.pos[dim] - b2.pos[dim]) * self.fragrance)


def intensity(expected, value, base):
    return max(0, base - abs(expected - value))


def iteration(population, modal, modalExp, prevBest, expected, contextSwitch):

    for i in range(len(population)):
        population[i].updateFragrance(modal, modalExp, expected)

    for i in range(len(population)):
        if uniform(0,1) < contextSwitch:
            population[i].globalSearch(prevBest)
        else:
            c1 = choice([x for x in range(len(population) - 1) if x != i])
            b1 = population[c1]
            b2 = population[ choice ( [ x for x in range ( len( population) - 1) if x not in [i, c1] ] ) ]
            population[i].localSearch(b1, b2)

    population.sort(key=lambda x: x.fitness(x.pos))
    best = population[0]

    return best

def passFunc(argTab):
    return simulation(argTab[0], argTab[1], argTab[2], argTab[3])

def simulation(args, func, minVal, maxVal):

    population = [Butterfly(args.dimensions, minVal, maxVal, func) for _ in range(args.popsize)]

    population.sort(key=lambda x: x.fitness(x.pos))
    best = population[0]
    iterCount = 0

    while iterCount < args.iterations and best.fitness(best.pos) > args.expected - args.tolerance:
        best = iteration(population, args.modal, args.modalExp, best, args.expected, args.contextSwitch)
        iterCount += 1
    
    return best



if __name__ == "__main__":

    # parser
    parser=argparse.ArgumentParser(description="BAT")
    parser.add_argument('-p','--popsize', type=int)
    parser.add_argument('-d','--dimensions',type=int)
    parser.add_argument('-a','--modalExp',type=float)
    parser.add_argument('-c','--modal',type=float)
    parser.add_argument('-r','--contextSwitch',type=float)
    parser.add_argument('-i','--iterations',type=int)
    parser.add_argument('-f','--function',type=str)
    parser.add_argument('-e','--expected',type=float)
    parser.add_argument('-t', '--tolerance', type=float)
    args=parser.parse_args()

    if args.function == 'f2':
        minVal = -100
        maxVal = 100
        func = f2
    elif args.function == 'rastrigin':
        minVal = -5.12
        maxVal = 5.12
        func = rastrigin
    elif args.function == 'zakharov':
        minVal = -10
        maxVal = 10
        func = zakharov
    else:
        print("Function not supported!")
        exit(666)

    if not args.iterations : args.iterations = 10000
    if not args.tolerance : args.tolerance = 0

    # results = simulation(args, func, minVal, maxVal)

    with Pool(processes = 10) as p:
        results = p.map(passFunc, [[args, func, minVal, maxVal] for _ in range(10)] )
        p.close()
        p.join()

    print( [r.fitness(r.pos) for r in results] )