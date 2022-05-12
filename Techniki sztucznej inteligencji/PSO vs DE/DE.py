from itertools import count
from math import inf
from multiprocessing import Manager, Pool
from random import randint, uniform
from copy import deepcopy
from numpy import multiply
from operator import add, sub
import argparse
from evaluation_functions import process
from test_functions import *

################################################################################################################################################################################################
##########################################################################    Classes    #######################################################################################################
################################################################################################################################################################################################

# class describing generation 0
class Parent:

    def __init__(self, geneCount, func, minVal, maxVal):

        self.generation = 0
        self.genes = [uniform(minVal, maxVal) for x in range(geneCount)]
        self.func = func


    def cross(self, mutantGenes, crossChance):

        newGenes = []

        for i, x in enumerate(self.genes):
            if uniform(0, 1) < crossChance:
                newGenes.append(self.genes[i])
            else:
                newGenes.append(mutantGenes[i])

        return Object(self.generation+1, newGenes, self.func)

    
    # fitness function, returning value from range [0,1]
    def value(self):
        return self.func(self.genes)

    def __eq__(self, other):
        return self.genes == other.genes and self.id == other.id

    def __hash__(self):
        return hash(('generation', self.generation, 'genes', str(self.genes), 'id', self.id))

################################################################################################################################################################################################

# class describing generations past 0'th, inherits all methods from Parent expcept for constructor
class Object(Parent):

    def __init__(self, generation, genes, func):

        self.generation = generation
        self.genes = genes
        self.func = func

################################################################################################################################################################################################
#######################################################################    End of classes    ###################################################################################################
################################################################################################################################################################################################


################################################################################################################################################################################################
#########################################################################    Functions    ######################################################################################################
################################################################################################################################################################################################

# create mutant to be used for crossing
def createMutant(particleList, ampRate):

    mutationBase = particleList[randint(0, len(particleList)-1)].genes

    firstDiff = particleList[randint(0, len(particleList)-1)].genes
    while firstDiff == mutationBase:
        firstDiff = particleList[randint(0, len(particleList)-1)].genes

    secondDiff = particleList[randint(0, len(particleList)-1)].genes
    while secondDiff == mutationBase or secondDiff == firstDiff:
        secondDiff = particleList[randint(0, len(particleList)-1)].genes

    return list(map(add, mutationBase, multiply(list(map(sub, firstDiff, secondDiff)), ampRate)))


# returns best object that matches minimal standard(set expectedFitness == 0 to guarantee result)
def checkGenerationBest(objects):

    result = None
    for object in objects:
        if not result or object.value() < result.value():
            result = object

    return result

# one iteration of the simulation
def progress(previousGeneration, ampRate, crossChance):
    
    # pre-declare lists to be used
    newGeneration = []
    mutantGenes = createMutant(previousGeneration, ampRate)

    for elem in previousGeneration:
        temp = elem.cross(mutantGenes, crossChance)
        if temp.value() < elem.value() : newGeneration.append(temp)
        else : newGeneration.append(elem)
    
    return newGeneration

################################################################################################################################################################################################

def passProc(procArgs):
    initiate(procArgs[0], procArgs[1], procArgs[2], procArgs[3], procArgs[4], procArgs[5], procArgs[6], procArgs[7], procArgs[8], procArgs[9], procArgs[10])

################################################################################################################################################################################################

# amount of cross points determines cross method
def initiate(populationSize, geneCount, crossChance, ampRate, iterations, tolerance, func, minVal, maxVal, bestList, bestVals):
    
    bestValueList = []

    # create generation 0
    currentGeneration = [Parent(geneCount, func, minVal, maxVal) for x in range(populationSize)]

    bestDataset = [checkGenerationBest(currentGeneration).value()]
    bestValues = [checkGenerationBest(currentGeneration).genes]

    counter = 0
    best = inf

    while counter < iterations and best > tolerance:

        previousGeneration = deepcopy(currentGeneration)
        currentGeneration = progress(previousGeneration, ampRate, crossChance)
        
        # get relevant data for plot from current generation
        bestDataset.append(checkGenerationBest(currentGeneration).value())
    
        counter += 1

    bestList.append(checkGenerationBest(currentGeneration).value())
    bestVals.append(bestDataset)

    # return checkGenerationBest(currentGeneration).value(), counter


################################################################################################################################################################################################
####################################################################    End of functions    ####################################################################################################
################################################################################################################################################################################################

if __name__ == '__main__':

    # parser
    parser=argparse.ArgumentParser(description="DE")
    parser.add_argument('-p','--popsize', type=int)
    parser.add_argument('-g','--geneCount',type=int)
    parser.add_argument('-c','--crossChance',type=float)
    parser.add_argument('-a','--ampRate',type=float)
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
    else:
        print("Function not supported!")
        exit(666)

    if not args.iterations : args.iterations = 10000
    if not args.tolerance : args.tolerance = 0
        
    m = Manager()
    bestList = m.list()
    bestVals = m.list()

    procArgs = []
    with Pool(processes=10) as pool:
        for x in range(10) : procArgs.append([args.popsize, args.geneCount, args.crossChance, args.ampRate, args.iterations, args.tolerance, func, minVal, maxVal, bestList, bestVals])
        pool.map(passProc, procArgs)
        pool.close()
        pool.join()

    res = process(bestList, bestVals)
    print(res)
    # run simulation for specified parameters

    

    # results, counter = initiate(args.popsize, args.geneCount, args.crossChance, args.ampRate, args.iterations, args.expected + args.tolerance, func, minVal, maxVal)

    # print("Value for best object: ", results)
    # print("Number of iterations: ", counter)