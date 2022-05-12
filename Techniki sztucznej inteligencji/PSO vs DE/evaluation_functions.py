import numpy
import matplotlib.pyplot as plt

def graph(x):
    plt.plot(x[0], color='green', label='best')
    plt.plot(x[-1], color='red', label='worst')
    plt.legend()
    plt.show()

def process(bestList, valuesLists):
    localList, localValues = [ list(tuple) for tuple in  zip(*sorted(zip(bestList, valuesLists)))]
    best = localList[0]
    worst = localList[-1]
    median = numpy.median(localList)
    avg = numpy.average(localList)
    std= numpy.std(localList)
    graph(localValues)
    return [best, worst, median, avg, std]

#print(process([76, 1, 32, 564], [[5,4,3,2,1], [1,2,3,4,5], [3,2,4,1,5], [9,1,7,2,4]]))

