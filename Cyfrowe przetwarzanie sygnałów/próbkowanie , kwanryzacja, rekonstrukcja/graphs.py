from matplotlib import pyplot as plt
from numpy import arange


def createCompareSignal(extentionRate, sampleRate, duration, func, args):
    temp = 1 / (extentionRate * (sampleRate))
    xCompare = arange(0, duration + temp, temp)
    yCompare = []

    for elem in xCompare:
        yCompare.append(func(elem, *args))

    return xCompare, yCompare

def addComlexPlot(x, y):
    plt.plot(x, y, color='green', linewidth = 2, label='Original', zorder=2)

def addComparePlot(extentionRate, sampleRate, duration, func, args):
    xCompare, yCompare = createCompareSignal(extentionRate, sampleRate, duration, func, args)
    plt.plot(xCompare, yCompare, color='green', linewidth = 2, label='Original', zorder=2)

def addSamplePlot(xSample, ySample):
    plt.scatter(xSample, ySample, color='blue', s = 10, label='Samples', zorder=3)

def addStepPlot(xSample, ySample):
    plt.step(xSample, ySample, color='red', linewidth = 1, alpha = 0.5, label='Result', where='post', zorder=1)

def addInterpolatedPlot(xInter, yInter):
    plt.plot(xInter, yInter, color='red', linewidth = 2, alpha = 0.5, label='Result', zorder=1)

def showPlot():
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()