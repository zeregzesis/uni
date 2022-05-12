from random import getrandbits, randint, choice, sample
from matplotlib import colors, use
from pandas import DataFrame
from math import floor
from copy import deepcopy
from matplotlib.pyplot import clf, plot, legend, savefig, subplots, title, close, ioff
from matplotlib.lines import Line2D
from os import mkdir, path

# used to generate unique id's for objects, useful to avoid object duplicates in subsequent generations
def uniqueid():
    seed = getrandbits(32)
    while True:
       yield seed
       seed += 1

################################################################################################################################################################################################
##########################################################################    Classes    #######################################################################################################
################################################################################################################################################################################################

# class describing item to be pun in knapsack
class Item:

    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

################################################################################################################################################################################################

# class describing generation 0
class Parent:

    def __init__(self, geneCount):

        self.id = next(unique_sequence)
        self.generation = 0
        self.genes = list([randint(0,1) for x in range(geneCount)])


    def cross(self, firstParentGenes, secondParentGenes, crossPoints):

        genes = []
        switch = 0
        previous = 0

        for x in crossPoints:
            if not switch:
                genes += firstParentGenes[previous:x]
                switch = 1
            else:
                genes += secondParentGenes[previous:x]
                switch = 0
            previous = x

        return genes

    
    # fitness function, returning value from range [0,1]
    def fitnessScore(self):
        
        weight = 0
        value = 0

        for x in range(len(self.genes)):
            if self.genes[x]:
                weight += itemList[x].weight
                value += itemList[x].value

        # if items don't fit, fitness is 0
        if weight > weightLimit:
            return 0

        # the closer value is to maxValue, the better
        return value / maxValue

    def mutate(self):
        randomGene = randint(0,len(self.genes)-1)
        if self.genes[randomGene]:
            self.genes[randomGene] = 0
        else:
            self.genes[randomGene] = 1

    def __eq__(self, other):
        return self.genes == other.genes and self.id == other.id

    def __hash__(self):
        return hash(('generation', self.generation, 'genes', str(self.genes), 'id', self.id))

################################################################################################################################################################################################

# class describing generations past 0'th, inherits all methods from Parent expcept for constructor
class Object(Parent):

    def __init__(self, generation, firstParentGenes, secondParentGenes, crossPoints):

        self.id = next(unique_sequence)
        self.generation = generation
        self.genes = self.cross(firstParentGenes, secondParentGenes, crossPoints)

################################################################################################################################################################################################
#######################################################################    End of classes    ###################################################################################################
################################################################################################################################################################################################

################################################################################################################################################################################################
######################################################################    Global variables    ##################################################################################################
################################################################################################################################################################################################

# disable interactive mode of pyplot to avoid errors with generating multiple figures
ioff()
use('Agg')

# instance used to generate said id's
unique_sequence = uniqueid()

# calculated using greedy approximation algorithm
maxValue = 13654201

#given as entry condition
weightLimit = 6404180

#items to select from
itemList =  [
                Item(   "Toporek",             32252,      68674   ),
                Item(   "Moneta z brązu",      225790,     471010  ),
                Item(   "Korona",              468164,     944620  ),
                Item(   "Diamentowy posążek",  489494,     962094  ),
                Item(   "Szmaragdowy pas",     35384,      78344   ),
                Item(   "Skamieliny",          265590,     579152  ),
                Item(   "Złota moneta",        497911,     902698  ),
                Item(   "Hełm",                800493,     1686515 ),
                Item(   "Tusz",                823576,     1688691 ),
                Item(   "Szkatułka",           552202,     1056157 ),
                Item(   "Nóż",                 323618,     677562  ),
                Item(   "Długi miecz",         382846,     833132  ),
                Item(   "Maska",               44676,      99192   ),
                Item(   "Naszyjnik",           169738,     376418  ),
                Item(   "Opalowa zawieszka",   610876,     1253986 ),
                Item(   "Perły",               854190,     1853562 ),
                Item(   "Kołczan",             671123,     1320297 ),
                Item(   "Rubinowy pierścień",  698180,     1301637 ),
                Item(   "Srebrna bransoletka", 446517,     859835  ),
                Item(   "Czasomierz",          909620,     1677534 ),
                Item(   "Mundur",              904818,     1910501 ),
                Item(   "Trucizna",            730061,     1528646 ),
                Item(   "Wełniany szal",       931932,     1827477 ),
                Item(   "Kusza",               952360,     2068204 ),
                Item(   "Stara księga",        926023,     1746556 ),
                Item(   "Puchar z cynku",      978724,     2100851 )
            ]
    
# last point must be the last index, so that last part of genome is carried over correctly
crossPoints = [ [ floor(len(itemList)/2), len(itemList) ], [ 5, 8, 17, len(itemList) ] ]

################################################################################################################################################################################################
##################################################################    End of global variables    ###############################################################################################
################################################################################################################################################################################################

################################################################################################################################################################################################
#########################################################################    Functions    ######################################################################################################
################################################################################################################################################################################################

# returns best object that matches minimal standard(set expectedFitness == 0 to guarantee result)
def checkGenerationFittness(objects, expectedFitness):
    """
    Checks for best object in generation that matches minimal standard
        Input:
            objects             -- List of objects representing generation
             expectedFitness    -- Minimal fitness score(set to 0 to guarantee result)
        Output:
            None        -- No object meets the minimal standard
             (or)<Object>   -- Best object that meets minimal standard
    """

    result = None
    for object in objects:
        if object.fitnessScore() >= expectedFitness:
            if not result or object.fitnessScore() >= result.fitnessScore():
                result = object

    return result

################################################################################################################################################################################################

# returns worst object that falls below standard(set expectedFitness == 1 to guarantee result)
def lowestGenerationFittness(objects, expectedFitness):
    """
    Checks for worst object in generation that goes below threshold
        Input:
            objects             -- List of objects representing generation
             expectedFitness    -- Maximum fitness score(set to 1 to guarantee result)
        Output:
            None        -- No object goes below threshold
             (or)<Object>   -- Worst object that goes below threshold
    """

    result = None
    for object in objects:
        if object.fitnessScore() <= expectedFitness:
            if not result or object.fitnessScore() < result.fitnessScore():
                result = object

    return result

# returns average fitness of given generation
def avgGenerationFittness(objects):
    """
    Checks for average fitness score in generation
        Input:
            objects -- List of objects representing generation
        Output:
            <float> -- Average fitness score
    """

    result = 0
    for object in objects:
        result += object.fitnessScore()

    return result / len(objects)

################################################################################################################################################################################################

# one iteration of the simulation
def progress(previousGeneration, selectionMethod, crossPointsLocal, crossChance, mutationChance, iteration):
    """
    Progress simulation to the next generation
        Input:
            previousGeneration  -- List of objects representing previous generation
             selectionMethod    -- Selection method indicator(0 for "ranking" method, 1 for "roulette" method)
            crossPointsLocal    -- Points at which crossing genes happen
             crossChance        -- % of previous generation selected to be crossed
            mutationChance      -- % of new generation to mutate
             iteration          -- Current iteration, and therefore current generation number indicator
        Output:
            <List<Object>>        -- List of objects representing new generation
    """
    
    # pre-declare lists to be used
    selected = []
    temp = []
    newGeneration = []

    # populate selected according to chosen method( 1 = roulette, 0 = ranking)
    if selectionMethod:
        # determining each object's chance at being drawn for crossing, fitness translates to chance

        for object in previousGeneration:
            selectionChance = 1 + floor(object.fitnessScore() * 10)

            for x in range(selectionChance):
                temp.append(object)

    else:
        # determining each object's chance at being drawn for crossing, position in ranking translates to chance
        
        # rank objects based on their fitness score(ascending)
        previousGeneration.sort(key=lambda x: x.fitnessScore())
        
        # the lower in the ranking(better fitness), the more chance to be chosen
        for x in range(1,len(previousGeneration)+1):
            for y in range(x):
                temp.append(previousGeneration[x-1])

    # choosing which objects to cross, one object can't be chosen more than once
    for x in range(floor(len(previousGeneration) * crossChance)):
        chosenObject = choice(temp)
        selected.append(chosenObject)

        # filter all ocurences of chosen object to avoid picking it multiple times
        temp = list(filter(lambda a: a != chosenObject, temp))

    # safeguard to avoid odd number of parents
    while len(selected) % 2:
        selected.append(choice(previousGeneration))
        selected = list(set(selected))


    # crossing selected objects
    while selected:
        firstParent = choice(selected)
        selected.remove(firstParent)
        if selected:
            secondParent = choice(selected)
            selected.remove(secondParent)
            newGeneration.append(Object(iteration, firstParent.genes, secondParent.genes, crossPointsLocal))
            newGeneration.append(Object(iteration, secondParent.genes, firstParent.genes, crossPointsLocal))

    # convert to set to make eliminating duplicates easier
    newGeneration = set(newGeneration)

    # filling the rest of new generation with objects from previous one
    while not len(newGeneration) == len(previousGeneration):
        newGeneration.add(choice(previousGeneration))

    # convert back to list for ease of use later
    newGeneration = list(newGeneration)
            
            
    # mutate new generation based on mutation chance
    for object in sample(newGeneration, floor(mutationChance * len(newGeneration))):
        object.mutate()

    return newGeneration

################################################################################################################################################################################################

# amount of cross points determines cross method
def initiate(populationSize, selectionMethod, crossPointsLocal, crossChance, mutationChance, iterations = 0):
    """
    Start the simulation with given parameters
        Input:
            populationSize      -- How many objects each generaion consists of
             selectionMethod    -- Selection method indicator(0 for "ranking" method, 1 for "roulette" method)
            crossPointsLocal    -- Points at which crossing genes happen
             crossChance        -- % of previous generation selected to be crossed
            mutationChance      -- % of new generation to mutate
             iteration          -- Current iteration, and therefore current generation number indicator
        Output:
            <List<Object>>                  -- List of objects representing last generation
             (and) <int>                    -- Last generation number
            (and) < List< List< float >>>   -- Data used for plot
    """
    
    # create generation 0
    currentGeneration = set([Parent(len(itemList)) for x in range(populationSize)])

    currentGeneration = list(currentGeneration)

    # get relevant data for plot from generation 0
    lowestDataset = [lowestGenerationFittness(currentGeneration, 1).fitnessScore()]
    avgDataset = [avgGenerationFittness(currentGeneration)]
    bestDataset = [checkGenerationFittness(currentGeneration, 0).fitnessScore()]

    if iterations:
        for iteration in range(iterations):
            previousGeneration = deepcopy(currentGeneration)
            currentGeneration = progress(previousGeneration, selectionMethod, crossPointsLocal, crossChance, mutationChance, iteration)
            
            # get relevant data for plot from current generation
            lowestDataset.append(lowestGenerationFittness(currentGeneration, 1).fitnessScore())
            avgDataset.append(avgGenerationFittness(currentGeneration))
            bestDataset.append(checkGenerationFittness(currentGeneration, 0).fitnessScore())


    # package plot data in a list
    graphStats = [lowestDataset, avgDataset, bestDataset]

    return currentGeneration, iteration, graphStats

################################################################################################################################################################################################

# create and save plot
def createGraph(graphData, plotpath, plotname):
    """
    Save plot of simulation data
        Input:
            graphData   -- 
             plotpath   -- 
            plotname    -- 
        Output:
            <List<Object>>                  -- List of objects representing last generation
             (and) <int>                    -- Last generation number
            (and) < List< List< float >>>   -- Data used for plot
    """

    x = [q for q in range(len(graphData[0]))]

    fig, ax = subplots(clear=True)

    ax.plot(x, graphData[2], color = 'green', alpha = 0.5, label = 'Best')
    ax.plot(x, graphData[1], color = 'yellow', alpha = 0.75, label = 'Average')
    ax.plot(x, graphData[0], color = 'red', label = 'Worst')

    
    legend(loc = 'upper right')

    savefig(plotpath+plotname)
    ax.cla()
    fig.clf()
    close('all')

################################################################################################################################################################################################
####################################################################    End of functions    ####################################################################################################
################################################################################################################################################################################################

if __name__ == '__main__':

    # specify path where data should be dumped
    filepath = "C:\\Users\\maste\\Desktop\\other\\meta_z3\\statistics\\"

    # specify path where plots should be dumped
    plotpath = "C:\\Users\\maste\\Desktop\\other\\meta_z3\\graphs\\"
    
    # cross method ( 0 = single point, 1 = 3 points) and points to cross at
    for cross in [0, 1]:

        # method( 1 = roulette, 0 = ranking)
        for selectionMethod in [0, 1]:

            # how many object per generation
            for populationSize in [10, 20, 50, 100]:

                # number of iterations to run
                for iterations in [25, 50, 100, 200]:

                    # excel format file name to dump results to
                    filename = str(cross) + "_" + str(selectionMethod) + "_" + str(populationSize) + "_" + str(iterations) + ".xlsx"

                    # create folder for dumping plots and specify path for said dump
                    plotSubPath = str(cross) + "_" + str(selectionMethod) + "_" + str(populationSize) + "_" + str(iterations)
                    try:
                        mkdir(path.join(plotpath,plotSubPath))
                    except:
                        pass
                    plotSubPath += "\\"

                    # pre-declare lists to be used for data collection
                    crossChanceColumn = []
                    mutationChanceColumn = []
                    xColumn = []
                    worstColumn = []
                    avgColumn = []
                    bestColumn = []

                    # % of population to select to cross
                    for crossChance in [0.25, 0.5, 0.75, 1.0]:

                        # % of population to mutate
                        for mutationChance in [0.0, 0.25, 0.5, 0.75]:
                            
                            # test each variation 5 times
                            for x in range(1,6):

                                # plot name that include conditions it describes
                                plotname = str(cross) + "_" + str(selectionMethod) + "_" + str(populationSize) + "_" + str(iterations) + "_" + str(crossChance) + "_" + str(mutationChance) + "_" + str(x) + ".png"

                                try:
                                    # run simulation for specified parameters
                                    results = initiate(populationSize, selectionMethod, crossPoints[cross], crossChance, mutationChance, iterations)
                                except:
                                    # if there's an error, fill data with -1 values for easy identification in dumped dataset
                                    worstColumn.append(-1)
                                    avgColumn.append(-1)
                                    bestColumn.append(-1)
                                else:
                                    # fill data with correct values
                                    worstColumn.append(lowestGenerationFittness(results[0], 1).fitnessScore())
                                    avgColumn.append(avgGenerationFittness(results[0]))
                                    bestColumn.append(checkGenerationFittness(results[0], 0).fitnessScore())
                                    
                                    # try creating a plot of collected data
                                    #try:
                                    createGraph(results[2], plotpath + plotSubPath, plotname)
                                    #except:
                                        #print("Problem with graph " + str(plotSubPath) + plotname)

                                finally:
                                    # add data that's not dependent on simulation success
                                    crossChanceColumn.append(crossChance)
                                    mutationChanceColumn.append(mutationChance)
                                    xColumn.append(x)

                            
                    # try dumping the data to excel file       
                    try:
                        data = {"Cross chance" : crossChanceColumn, "Mutation chance" : mutationChanceColumn, "Sample" : xColumn, "Worst" : worstColumn, "Avg" : avgColumn, "Best" : bestColumn}
                        df = DataFrame(data, columns = ["Cross chance", "Mutation chance", "Sample", "Worst", "Avg", "Best"])
                        df.to_excel (filepath + filename, index = False, header = True)
                    except:
                        print("Problem with file " + filename)
                    finally:
                        print("Done with " + plotSubPath)
                        #input("Excel pause")