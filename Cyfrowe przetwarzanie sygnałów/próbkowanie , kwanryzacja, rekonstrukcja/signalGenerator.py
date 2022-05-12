import operator
import matplotlib.pyplot as plt
from numpy import arange, unique, isclose
from numpy.random import normal, uniform
from math import pi, sin, sqrt
from pickle import dump, load
from signalSampling import *

##############################################################################################################################

def graph(x, func, params, y = None):
    if not y : y = [func(value, *params) for value in x]
    plt.plot(x, y)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.show()
    return y

def graphDis(x, func, params, y = None):
    if not y : y = [func(value, *params) for value in x]
    plt.scatter(x, y)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.show()
    return y

def graphHist(y, bins, T = None):

    plt.hist(statLimit(y, T) if T else y, bins, rwidth=0.85)
    plt.xlabel("Values")
    plt.ylabel("Count")
    plt.show()

def graphOperation(x1, x2, x3, y1, y2, y3):

    plt.subplot(1, 3, 1)
    plt.plot(x1, y1)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("First signal")

    plt.subplot(1, 3, 2)
    plt.plot(x2, y2)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Second signal")

    plt.subplot(1, 3, 3)
    plt.plot(x3, y3)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Result signal")

    plt.tight_layout()
    plt.show()

##############################################################################################################################

def statLimit(x, T):
    return x[:int((len(x) / T) * T)]

def signalAvg(y, T = None):
    if T : y = statLimit(y, T)
    return sum(y) / len(y)

def signalAbsAvg(y, T = None):
    if T : y = statLimit(y, T)
    return sum([abs(elem) for elem in y]) / len(y)

def signalAvgPow(y, T = None):
    if T : y = statLimit(y, T)
    return sum([elem**2 for elem in y]) / len(y)

def signalVar(y, T = None):
    if T : y = statLimit(y, T)
    sigAvg = signalAvg(y, T)
    return sum([(elem - sigAvg)**2 for elem in y]) / len(y)

def signalEff(y, T = None):
    if T : y = statLimit(y, T)
    return sqrt(signalAvgPow(y, T))

def allStats(y, T = None):
    return [round(signalAvg(y, T), 2), round(signalAbsAvg(y, T), 2), round(signalAvgPow(y, T), 2), round(signalVar(y, T), 2), round(signalEff(y, T), 2)]

##############################################################################################################################

def signalOperation(x1, x2, y1, y2, operator):
    tempX = x1 + x2
    tempY = y1 + y2
    tempX, tempY = zip(*sorted(zip(tempX, tempY)))
    result = []
    prevX = -1000
    prevY = -1000

    for i, val in enumerate(tempY):
        if isclose(prevX, tempX[i], rtol=1e-04, atol=1e-08, equal_nan=False):
            result.pop()
            try:
                result.append(operator(prevY, val))
            except ZeroDivisionError:
                result.append(0)
        else:
            result.append(val)
        prevX = tempX[i]
        prevY = val
    return list(unique([round(elem, 6) for elem in tempX])), result

##############################################################################################################################

def RandomNoice(x, amp):
    return uniform(-amp, amp)
    
def GauusNoice(x, amp):
    return normal(0, 1) * amp / 3

def SinSignal(x, amp, T, t0):
    return amp * sin( (2 * pi / T) * (x - t0) )
    
def SinSingleHalfFlatSignal(x, amp, T, t0):
    return 0.5 * amp * ( sin( (2 * pi / T) * (x - t0) ) + abs( sin( (2 * pi / T) * (x - t0) ) ) )
    
def SinDoubleHalfFlatSignal(x, amp, T, t0):
    return amp * abs( sin( (2 * pi / T) * (x - t0) ) )
    
def RectSignal(x, amp, T, t0, k, sym = None):
    kT = int(x / T) * T
    if kT + t0 <= x < k * T + kT + t0 :
        return amp
    if sym : return -amp
    return 0

def triangleSignal(x, amp, T, t0, k):
    kT = int(x / T) * T
    return (amp / (k * T) ) * (x - kT - t0) if kT + t0 <= x < k * T + kT + t0 else amp + ( -amp / (T * (1 - k)) ) * (x - kT - t0) + (amp / 1 - k)

def unitJump(x, amp, jumpTime):
    if x < jumpTime : return 0
    return 0.5 * amp if x == jumpTime else amp

def singlePulse(x, pulseTime):
    return 1 if x == pulseTime else 0

def pulseNoice(x, chance):
    return 1 if uniform(0, 1) <= chance else 0

##############################################################################################################################
    
