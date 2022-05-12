import argparse
from random import gauss, uniform
from numpy import exp, inf
from multiprocessing import Manager, Pool

from test_functions import f2, rastrigin, zakharov
from evaluation_functions import process

class Bat:
    def __init__(self, dim, fMin, fMax, min, max, fitness, loudness, pulseRate):
        self.pos = [uniform(min, max) for _ in range(dim)]
        self.tempPos = self.pos.copy()
        self.vel = [0 for _ in range(dim)]
        self.fitness = fitness
        self.loudness = loudness
        self.pulseRate = pulseRate
        self.solution = fitness(self.pos)
        self.tempSolution = self.solution
        self.fMin = fMin
        self.fMax = fMax
        self.min = min
        self.max = max
        self.freq = 0.0

    def bound(self):
        for i in range(len(self.pos)):
            if self.pos[i] < self.min:
                self.pos[i] = self.min
            elif self.pos[i] > self.max:
                self.pos[i] = self.max

    def boundTemp(self):
        for i in range(len(self.tempPos)):
            if self.tempPos[i] < self.min:
                self.tempPos[i] = self.min
            elif self.tempPos[i] > self.max:
                self.tempPos[i] = self.max

    def updateSolution(self):
        self.solution = self.fitness(self.pos)

    def updateTempSolution(self):
        self.tempSolution = self.fitness(self.tempPos)

    def updateFreq(self):
        self.freq = self.fMin + (self.fMax - self.fMin) * uniform(0,1)

    def updateVel(self, best):
        for i in range(len(self.vel)):
            self.vel[i] = self.vel[i] + (self.pos[i] - best.pos[i]) * self.freq
    
    def updatePos(self):
        for i in range(len(self.pos)):
            self.pos[i] = self.pos[i] + self.vel[i]

    def updateTempPos(self):
        for i in range(len(self.tempPos)):
            self.tempPos[i] = self.tempPos[i] + self.vel[i]

    def moveToPulse(self, best, loudnessAvg):
        for i in range(len(self.tempPos)):
            self.tempPos[i] = best.pos[i] * loudnessAvg * gauss(0, 1)

    def updateLoudness(self, alpha):
        self.loudness *= alpha

    def updatePulseRate(self, gamma, iter):
        self.pulseRate *= (1 - exp(-gamma * iter))

    def move(self, best, loudnessAvg, alpha, gamma, iter):
        self.updateFreq()
        self.updateLoudness(alpha)
        self.updatePulseRate(gamma, iter)
        self.updateVel(best)
        self.updateTempPos()
        self.boundTemp()
        if uniform(0,1) > self.pulseRate:
            self.moveToPulse(best, loudnessAvg)
            self.bound()
        self.updateTempSolution()
        if (self.tempSolution <= self.solution) and (uniform(0, 1) < self.loudness):
            self.pos = self.tempPos.copy()
            self.bound()
            self.updateSolution()

def iteration(population, best, alpha, gamma, iter):

    loudnessAvg = 0
    for i in range(len(population)):
        loudnessAvg += population[i].loudness
    loudnessAvg /= len(population)

    for bat in population:
        bat.move(best, loudnessAvg, alpha, gamma, iter)

    sortedPop = sorted(population, key=lambda x: x.fitness(x.pos))
    best = sortedPop[0] if sortedPop[0].solution < best.solution else best
    return best

def passFunc(args):
    return simulation(args[0], args[1], args[2], args[3], args[4], args[5])

def simulation(args, fitness, minVal, maxVal, bestList, bestVals):

    bestValueList = []
    
    population = [Bat(args.dimensions, args.fMin, args.fMax, minVal, maxVal, fitness, 0.5, 0.5) for _ in range(args.popsize)]

    population.sort(key=lambda x: x.fitness(x.pos))
    best = population[0]

    iterCount = 0

    while iterCount < args.iterations and best.fitness(best.pos) > args.expected - args.tolerance:
        best = iteration(population, best, args.alpha, args.gamma, iterCount)
        iterCount += 1
        bestValueList.append(best.solution)
    
    bestList.append(best.solution)
    bestVals.append(bestValueList)

    return best
        

if __name__ == '__main__':

    m = Manager()
    bestList = m.list()
    bestVals = m.list()

    # parser
    parser=argparse.ArgumentParser(description="BAT")
    parser.add_argument('-p','--popsize', type=int)
    parser.add_argument('-d','--dimensions',type=int)
    parser.add_argument('-fm','--fMin',type=float)
    parser.add_argument('-fM','--fMax',type=float)
    parser.add_argument('-a','--alpha',type=float)
    parser.add_argument('-g','--gamma',type=float)
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

    procArgs=[]
    with Pool(processes = 10) as p:
        # results = p.map(simulation, [[args, func, minVal, maxVal] for _ in range(10)])
        for x in range(10): procArgs.append([args, func, minVal, maxVal, bestList, bestVals])
        p.map(passFunc, procArgs)
        p.close()
        p.join()

    res = process(bestList, bestVals)
    print(res)

    # print(results.fitness(results.pos))