from math import inf
from random import uniform
from operator import add
import argparse
from evaluation_functions import process
from test_functions import *
from multiprocessing import Pool, Manager, freeze_support

class Particle:

    def __init__(self, min, max, func, dim):
        self.min = min
        self.max = max
        self.func = func
        self.value = inf
        self.pos = [uniform(min, max) for x in range(dim)]
        self.bestPos = self.pos
        self.vel = [0 for x in range(dim)]
        self.getValue()
    
    def getValue(self):
        if self.value > self.func(self.pos):
            self.bestPos = self.pos
        self.value = self.func(self.pos)
        return self.value

    def rebound(self):
        for i, dim in enumerate(self.pos):
            self.pos[i] = max(min(self.pos[i], self.max), self.min)

    def getBestValue(self):
        return self.func(self.bestPos)





def passProc(procArgs):
    proc(procArgs[0], procArgs[1], procArgs[2], procArgs[3], procArgs[4], procArgs[5])

def proc(minVal, maxVal, func, args, bestList, bestVals):

    swarm = []
    BestInSwarm = []
    bestValueList = []
    
    #initializing swarm
    for i in range(args.popsize):
        particle = Particle(minVal, maxVal, func, args.dimentions)
        swarm.append(particle)


    #choosing the best particle in initialized swarm
    currentBest = sorted(swarm, key=lambda x: x.getBestValue())[0]
    BestInSwarm.append(currentBest.getBestValue())

    #the most important loop of algorithm
    counter = 0
    best = inf
    inertiaWeight = 0.8
    if not args.iterations : args.iterations = 10000
    if not args.tolerance : args.tolerance = 0
    while counter < args.iterations and best > args.expected + args.tolerance :
        for particle in swarm:
            for i, d in enumerate(particle.pos):

                rp = uniform(0,1)
                rg = uniform(0,1)

                particle.vel[i] = -1 * inertiaWeight * particle.vel[i] + args.cognitiveCoeff * rp * (particle.bestPos[i] - particle.pos[i]) + args.socialCoeff * rg * (currentBest.bestPos[i] - particle.pos[i])

            particle.pos = list(map(add, particle.pos, particle.vel))
            particle.rebound()
            particle.getValue()

        currentBest = sorted(swarm, key=lambda x: x.getValue())[0]
        BestInSwarm.append(currentBest.getBestValue())

        inertiaWeight = 0.8 - (((0.8 - 0.1) / args.iterations) * counter)

        counter += 1
        best = currentBest.getBestValue()
        bestValueList.append(best)

    bestList.append(currentBest.getBestValue())
    bestVals.append(bestValueList)

    print("Parameters for best particle: ", currentBest.pos, "; Value for best particle: ", best, "; Number of iterations: ", counter)


if __name__ == '__main__':
    
    swarm = []
    BestInSwarm = []
    swarmBest = inf
    inertiaWeight = 0.8

    m = Manager()
    bestList = m.list()
    bestVals = m.list()

    parser=argparse.ArgumentParser(description="PSO")
    parser.add_argument('-p','--popsize', type=int)
    parser.add_argument('-i','--iterations',type=int)
    parser.add_argument('-c','--cognitiveCoeff',type=float)
    parser.add_argument('-s','--socialCoeff',type=float)
    parser.add_argument('-d','--dimentions',type=int)
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
    else:
        print("Function not supported!")
        exit(666)

    procArgs = []
    with Pool(processes=10) as pool:
        for x in range(10) : procArgs.append([minVal, maxVal, func, args, bestList, bestVals])
        pool.map(passProc, procArgs)
        pool.close()
        pool.join()

    res = process(bestList, bestVals)
    print(res)

    '''
    bestList = []
    bestVals = []
    for i in range(10):

        bestValueList = []
    
        #initializing swarm
        for i in range(args.popsize):
            particle = Particle(minVal, maxVal, func, args.dimentions)
            swarm.append(particle)


        #choosing the best particle in initialized swarm
        currentBest = sorted(swarm, key=lambda x: x.getBestValue())[0]
        BestInSwarm.append(currentBest.getBestValue())

        #the most important loop of algorithm
        counter = 0
        best = inf
        if not args.iterations : args.iterations = 100000
        if not args.tolerance : args.tolerance = 0
        while counter < args.iterations and best > args.expected + args.tolerance :
            for particle in swarm:
                for i, d in enumerate(particle.pos):

                    rp = uniform(0,1)
                    rg = uniform(0,1)

                    particle.vel[i] = -1 * inertiaWeight * particle.vel[i] + args.cognitiveCoeff * rp * (particle.bestPos[i] - particle.pos[i]) + args.socialCoeff * rg * (currentBest.bestPos[i] - particle.pos[i])

                particle.pos = list(map(add, particle.pos, particle.vel))
                particle.rebound()
                particle.getValue()

            currentBest = sorted(swarm, key=lambda x: x.getValue())[0]
            BestInSwarm.append(currentBest.getBestValue())

            inertiaWeight = 0.8 - (((0.8 - 0.1) / args.iterations) * counter)

            counter += 1
            best = currentBest.getBestValue()
            bestValueList.append(best)

        bestList.append(currentBest.getBestValue())
        bestVals.append(bestValueList)

        print("Parameters for best particle: ", currentBest.pos)
        print("Value for best particle: ", best)
        print("Number of iterations: ", counter)
    #'''  