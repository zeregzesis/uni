import glob
import os
from math import sqrt
from random import choice, choices
from decimal import Decimal
from matplotlib.pyplot import plot, legend, savefig, title, close, ioff
from matplotlib import use
from multiprocessing import Pool
from textwrap import wrap
from pylab import rcParams

# graph optimizations
ioff()
use('Agg')
rcParams["axes.titlesize"] = 8

# unchanging parameters
randomChance = 0.3
iterationCount = 1000

# indirect path to data files
path = './data/'

# class reprezention locations to visit
class Atraction:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y
    
    def __eq__(self, comp):
        return (True if self.number == comp.number else False)

    def __hash__(self) -> int:
        return hash(self.number)

# class representing individual ant
class Ant:

    def __init__(self, atractionList):
        if len(atractionList) == 0:
            print("wtf")
        self.visitedAtractions = []

        # random starting point
        self.visitedAtractions.append(choice(atractionList))

    def decide(self, atractionList, pathTable, alphaWeight, betaWeight, random = 0):

        # remove all visited
        tempList = [a for a in atractionList if a not in self.visitedAtractions]
        
        # first atraction can be random
        if choice([x for x in range(1,101)]) < random * 10:

            # making 100% sure we don't visit same atraction twice(shouldn't happen, but we already have function for that, so why not)
            while not self.visit(choice(tempList)):
                pass

        else:
            # everything is in Decimal, because sometimes feromone values get so low they're rounded to 0

            # calculate chances
            chance = []
            divisor = Decimal(0.0)

            # chances for every possible route based on feromones and heuristic(path length)
            for i in range(len(tempList)):
                pathResult = Decimal(pow(pathTable[frozenset( [ tempList[i], self.visitedAtractions[-1] ] )], alphaWeight)) * Decimal(pow(1/distance(tempList[i], self.visitedAtractions[-1]), betaWeight))
                divisor += pathResult
                chance.append(pathResult),

            # normalize chances to 100% and convert to float, since choices doesn't handle Decimal
            for i in range(len(chance)):
                chance[i] /= divisor
                chance[i] = float(chance[i])

            # chose atraction to visit(choices returns list, in our case with only one element in it, so [0] is to extract value from list)
            selected = choices(population=tempList, weights=chance, k=1)[0]

            # we should never enter into the 'while' body, but who knows...
            while not self.visit(selected):
                # remove from list to avoid selecting same atraction over and over
                del chance[tempList.index(selected)]
                tempList.remove(selected)
                selected = choices(population=tempList, weights=chance)

    # we should always get True out of this based on decide function logic, but better be safe than have calculations stop halfway through due to a simple error
    def visit(self, atraction):
        if atraction in self.visitedAtractions : return False
        self.visitedAtractions.append(atraction)
        return True

    # update feromones on paths that this ant visited
    def updateFeromones(self, pathTable):
        for i in range(1,len(self.visitedAtractions)):
            pathTable[ frozenset( [ self.visitedAtractions[i-1], self.visitedAtractions[i] ] ) ] += Decimal(1 / combinedDistance(self.visitedAtractions))
            

# get distance between to locations(length of path from one to another)
def distance(firstAtraction, secondAtraction):
    return sqrt(pow(abs(firstAtraction.x - secondAtraction.x), 2) + pow(abs(firstAtraction.y - secondAtraction.y), 2))

# get distance of the entire path taken
def combinedDistance(visited):
    if visited == None : return 0
    result = 0
    for i in range(1, len(visited)):
        result += distance(visited[i-1], visited[i])
    return result

# one iteration of a simulation
def iteration(population, alphaWeight, betaWeight, evaporationRate, atractionList, pathTable, random = 0):

    # create ant population with starting locations
    ants = []
    for pop in range(population):
        ants.append(Ant(atractionList))

    # choose next atraction to visit for every ant until no more atractions can be visited
    for x in range(1, len(atractionList)):
        for ant in ants:
            ant.decide(atractionList, pathTable, alphaWeight, betaWeight, random)

    # evaporate feromones
    for pair in pathTable:
        pathTable[pair] *= Decimal(evaporationRate)

    # leave new feromones and determine best path in generation
    bestPath = None
    for ant in ants:
        ant.updateFeromones(pathTable)
        if combinedDistance(ant.visitedAtractions) > combinedDistance(bestPath) : bestPath = ant.visitedAtractions    
    
    return bestPath


# save simulation results as a graph of path taken; graph name represents name of data file and simulation parameters, graph title shows shortest found path
def saveGraph(visited, name, pathTaken):

    x = [i for i in range(1,len(visited)+1)]
    y = [0]

    for i in range(len(visited)-1):
        y.append(distance(visited[i], visited[i+1]))

    plot(x, y, color = 'blue', marker = '*', label = 'Distance traveled = ' + str(round(combinedDistance(visited), 3)))

    legend(loc = 'upper right')

    title("\n".join(wrap(pathTaken, 80)))

    savefig(os.path.join("./plots/", name[7:]))

    close('all')

# workaround to call multi-argument function from pool.map method(multiprocessing)
def passFunc(tab):
    procFunc(tab[0], tab[1], tab[2], tab[3], tab[4], tab[5], tab[6])


# one simulation with given parameters
def procFunc(filename, population, alphaWeight, betaWeight, evaporationRate, atractionList, t):

    # feromones on all paths start at same value
    pathTable = {}
    for x in range(len(atractionList)):
        for y in range(x+1,len(atractionList)):
            pathTable[ frozenset( [ atractionList[x], atractionList[y] ] ) ] = Decimal(1.0)

    # run simulation
    try:
        # first iteration
        best = iteration(population, alphaWeight, betaWeight, evaporationRate, atractionList, pathTable, randomChance)

        # subsequent iterations
        for i in range(1, iterationCount):

            bestInIteration = iteration(population, alphaWeight, betaWeight, evaporationRate, atractionList, pathTable)

            # determine current best path
            if combinedDistance(bestInIteration) > combinedDistance(best):
                best = bestInIteration
        
        # convert Atraction class objects to numbers representing those locations
        finalPath = [o.number for o in best]

        # save results as a graph
        try:    
            saveGraph(best, str(filename) + "_trial=" + str(t) + "_pop=" + str(population) + "_alpha=" + str(alphaWeight) + "_beta" + str(betaWeight) + "_evap=" + str(evaporationRate) + ".png", str(finalPath))
        except:
            print("Take " + str(t) + " : Error with graph")

    except:
        print("Take " + str(t) + " : Error with simulation")


if __name__ == "__main__":
    # for every file
    for filename in glob.glob(os.path.join(path, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            
            # console print to give some sense of progress
            print("File : " + filename)

            # get all atractions from file
            atractionList = []
            for line in f:
                number, x, y = [int(x) for x in line.split()]
                atractionList.append(Atraction(number, x, y))

            # number of ants
            for population in [10, 30, 50]:

                # weight for feromones
                for alphaWeight in [1, 2]:
                    
                    # daclare worker pool to run multiple simulations in parallel
                    with Pool(processes=20) as pool:

                        argList = []
                        params = "parameters ( population = " + str(population) + ", alphaWeight = " + str(alphaWeight) + " )"

                        # weight for heuristic(path lenght)
                        for betaWeight in [1, 3]:

                            # rate of feromone evaporation
                            for evaporationRate in [0.1, 0.5]:
                                for t in range(1,6):
                                    argList.append([filename, population, alphaWeight, betaWeight, evaporationRate, atractionList, t])
                    
                        # start 20 simulations and wait for them to finish
                        pool.map(passFunc, argList)
                        pool.close()
                        pool.join()

                        # console print to give some sense of progress
                        print("Done with " + params)