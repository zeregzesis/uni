# x, y, funcName, args = loadFromFile(filename)

from numpy import arange
import numpy
from signalGenerator import *
from graphs import *
from util import *

### Próbkowanie ###

def sampleSignal(func, args, extentionRate, sampleRate, duration, plot = False):

    temp = 1 / (sampleRate)
    
    xSample = arange(0, duration + temp, temp)
    ySample = []

    for x in xSample:
        ySample.append(func(x, *args))

    if plot:
        addComparePlot(extentionRate, sampleRate, duration, func, args)
        addSamplePlot(xSample, ySample)
        showPlot()

    return xSample, ySample

def sampleComplex(x, y, sampleRate, plot = False):

    xSample = x[::int(1/sampleRate)]
    ySample = y[::int(1/sampleRate)]

    if xSample[-1] != x[-1]:
        xSample.append(x[-1])
        ySample.append(y[-1])

    if plot:
        addComlexPlot(x, y)
        addSamplePlot(xSample, ySample)
        showPlot()

    return xSample, ySample


### Interpolacja z sinc ###

def interpolateSingleValue(t, x, y):

    t = numpy.array(t)
    t.resize(1)

    u = numpy.resize(t, (len(x), len(t)))
    v = (x - u.T) / (x[1] - x[0])
    m = y * numpy.sinc(v)
    y_at_t = numpy.sum(m, axis = 1)

    return float(y_at_t)

def sincInterpolation(xSample, ySample, extentionRate, sampleRate, duration, func, args, complexX = None, complexY = None, plot = False):

    xExtended = []
    yExtended = []

    T = xSample[1] - xSample[0]

    if complexX : extentionRate = int(1 / sampleRate)

    for i in range(len(ySample) - 1):
        xExtended.append(xSample[i])
        yExtended.append(ySample[i])
        for j in range(1, extentionRate):
            step = (j/extentionRate) * T
            xExtended.append(xSample[i] + step)
            yExtended.append(interpolateSingleValue(xSample[i] + step, xSample, ySample))
    yExtended.append(ySample[-1])
    xExtended.append(xSample[-1])
    
    if plot:
        if complexX and complexY:
            addComlexPlot(complexX, complexY)
        else:
            addComparePlot(extentionRate, sampleRate, duration, func, args)
        addSamplePlot(xSample, ySample)
        addInterpolatedPlot(xExtended, yExtended)
        showPlot()

    return yExtended


### Kwantyzacja ###

def quantNoRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, func, args, complexX = None, complexY = None, plot = False):
    
    yShift = []

    if complexX : extentionRate = int(1 / sampleRate)

    for i in range(len(ySample)):
        yShift.append(roundPartial(ySample[i], roundRes))

    xQuant = []
    T = xSample[1] - xSample[0]
    for i in range(len(xSample) - 1):
        for j in range(extentionRate):
            step = (j/extentionRate) * T
            xQuant.append(xSample[i] + step)
    xQuant.append(xSample[-1])

    yQuant = []
    for i in range(len(yShift) - 1):
        yQuant += [yShift[i] for _ in range(int(extentionRate))]
    yQuant.append(yShift[-1])


    if plot:
        if complexX and complexY:
            addComlexPlot(complexX, complexY)
        else:
            addComparePlot(extentionRate, sampleRate, duration, func, args)
        addSamplePlot(xSample, ySample)
        addStepPlot(xQuant, yQuant)
        showPlot()

    return yQuant

def quantRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, func, args, complexX = None, complexY = None, plot = False):
    
    diff = (xSample[1] - xSample[0]) / 2.0

    if complexX : extentionRate = int(1 / sampleRate)
    
    xShift = [x - diff for x in xSample if x != xSample[0]]
    xShift.insert(0, xSample[0])

    yShift = []

    for i in range(len(ySample)):
        yShift.append(roundPartial(ySample[i], roundRes))

    xQuant = []
    T = xSample[1] - xSample[0]
    for i in range(len(xShift) - 1):
        for j in range(extentionRate):
            step = (j/extentionRate) * T
            xQuant.append(xSample[i] + step)
    xQuant.append(xSample[-1])

    yQuant = [yShift[0] for _ in range(int(extentionRate / 2))]
    for i in range(1, len(yShift) - 1):
        yQuant += [yShift[i] for _ in range(int(extentionRate))]
    yQuant += [yShift[-1] for _ in range(int(extentionRate / 2) + 1)]

    if plot:
        if complexX and complexY:
            addComlexPlot(complexX, complexY)
        else:
            addComparePlot(extentionRate, sampleRate, duration, func, args)
        addSamplePlot(xSample, ySample)
        addStepPlot(xQuant, yQuant)
        showPlot()
    
    return yQuant
    
### Eksrapolacja zerowego rzędu ###

def zeroOrderExtrapolation(xSample, ySample, extentionRate, sampleRate, duration, func, args, complexX = None, complexY = None, plot = False):

    if complexX : extentionRate = int(1 / sampleRate)

    xExtra = []
    T = xSample[1] - xSample[0]
    for i in range(len(xSample) - 1):
        for j in range(extentionRate):
            step = (j/extentionRate) * T
            xExtra.append(xSample[i] + step)
    xExtra.append(xSample[-1])

    yExtra = []
    for i in range(len(ySample) - 1):
        yExtra += [ySample[i] for _ in range(int(extentionRate))]
    yExtra.append(ySample[-1])

    

    if plot:
        if complexX and complexY:
            addComlexPlot(complexX, complexY)
        else:
            addComparePlot(extentionRate, sampleRate, duration, func, args)
        addSamplePlot(xSample, ySample)
        addStepPlot(xExtra, yExtra)
        showPlot()

    return yExtra  
    

### Interpolacja pierwszego rzędu ###

def firstOrderInterpolation(xSample, ySample, extentionRate, sampleRate, duration, func, args, complexX = None, complexY = None, plot = False):

    xExtended = []
    yExtended = []

    if complexX : extentionRate = int(1 / sampleRate)

    for i in range(len(ySample) - 1):
        lin = linFunc((xSample[i], ySample[i]), (xSample[i+1], ySample[i+1]))
        for j in range(extentionRate):
            xExtended.append(xSample[i] + (j/extentionRate) * (xSample[i+1] - xSample[i]))
            yExtended.append(lin(xSample[i] + (j/extentionRate) * (xSample[i+1] - xSample[i])))
    yExtended.append(ySample[-1])
    xExtended.append(xSample[-1])

    if plot:
        if complexX and complexY:
            addComlexPlot(complexX, complexY)
        else:
            addComparePlot(extentionRate, sampleRate, duration, func, args)
        addSamplePlot(xSample, ySample)
        addInterpolatedPlot(xExtended, yExtended)
        showPlot()
    
    return yExtended


if __name__ == '__main__':

    extentionRate = 10
    sampleRate = 10
    duration = 10
    amp = 20
    T = 5
    t0 = 0
    roundRes = 0.1
    k = 0.5

    '''
##############################################################################################################################

    # SinSingleHalfFlatSignal #
    print("SinSingleHalfFlatSignal")

    xOrig, yOrig = sampleSignal(SinSingleHalfFlatSignal, (amp, T, t0), 10, sampleRate * 10, duration)
    xSample, ySample = sampleSignal(SinSingleHalfFlatSignal, (amp, T, t0), extentionRate, sampleRate, duration)

    print("quantNoRound: ")
    res = quantNoRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, SinSingleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("quantRound: ")
    res = quantRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, SinSingleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("zeroOrderExtrapolation: ")
    res = zeroOrderExtrapolation(xSample, ySample, extentionRate, sampleRate, duration, SinSingleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("firstOrderInterpolation: ")
    res = firstOrderInterpolation(xSample, ySample, extentionRate, sampleRate, duration, SinSingleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("sincInterpolation")
    res = sincInterpolation(xSample, ySample, extentionRate, sampleRate, duration, SinSingleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print()
    
##############################################################################################################################

    # SinDoubleHalfFlatSignal #
    print("SinDoubleHalfFlatSignal")

    xOrig, yOrig = sampleSignal(SinDoubleHalfFlatSignal, (amp, T, t0), 10, sampleRate * 10, duration)
    xSample, ySample = sampleSignal(SinDoubleHalfFlatSignal, (amp, T, t0), extentionRate, sampleRate, duration)

    print("quantNoRound: ")
    res = quantNoRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, SinDoubleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("quantRound: ")
    res = quantRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, SinDoubleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("zeroOrderExtrapolation: ")
    res = zeroOrderExtrapolation(xSample, ySample, extentionRate, sampleRate, duration, SinDoubleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("firstOrderInterpolation: ")
    res = firstOrderInterpolation(xSample, ySample, extentionRate, sampleRate, duration, SinDoubleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("sincInterpolation")
    res = sincInterpolation(xSample, ySample, extentionRate, sampleRate, duration, SinDoubleHalfFlatSignal, (amp, T, t0), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print()

##############################################################################################################################
    '''
    # RectSignal #
    print("RectSignal")

    xOrig, yOrig = sampleSignal(RectSignal, (amp, T, t0, k), 10, sampleRate * 10, duration)
    xSample, ySample = sampleSignal(RectSignal, (amp, T, t0, k), extentionRate, sampleRate, duration)

    print("quantNoRound: ")
    res = quantNoRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, RectSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("quantRound: ")
    res = quantRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, RectSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("zeroOrderExtrapolation: ")
    res = zeroOrderExtrapolation(xSample, ySample, extentionRate, sampleRate, duration, RectSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("firstOrderInterpolation: ")
    res = firstOrderInterpolation(xSample, ySample, extentionRate, sampleRate, duration, RectSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("sincInterpolation")
    res = sincInterpolation(xSample, ySample, extentionRate, sampleRate, duration, RectSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print()


##############################################################################################################################

    # triangleSignal #
    print("triangleSignal")

    xOrig, yOrig = sampleSignal(triangleSignal, (amp, T, t0, k), 10, sampleRate * 10, duration)
    xSample, ySample = sampleSignal(triangleSignal, (amp, T, t0, k), extentionRate, sampleRate, duration)

    print("quantNoRound: ")
    res = quantNoRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, triangleSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("quantRound: ")
    res = quantRound(xSample, ySample, roundRes, extentionRate, sampleRate, duration, triangleSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("zeroOrderExtrapolation: ")
    res = zeroOrderExtrapolation(xSample, ySample, extentionRate, sampleRate, duration, triangleSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("firstOrderInterpolation: ")
    res = firstOrderInterpolation(xSample, ySample, extentionRate, sampleRate, duration, triangleSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))

    print("sincInterpolation")
    res = sincInterpolation(xSample, ySample, extentionRate, sampleRate, duration, triangleSignal, (amp, T, t0, k), complexX = None, complexY = None, plot = True)
    print(getAllMetrics(yOrig, res))