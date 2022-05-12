import operator
import matplotlib.pyplot as plt
from numpy import arange, unique, isclose
from numpy.random import normal, uniform
from math import pi, sin, sqrt
from pickle import dump, load

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

def saveToFile(x, y, args, funcName, filename):
    dump((x, y, funcName, args), open(filename, 'wb'))

def loadFromFile(filename):
    return load(open(filename, 'rb'))

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
    
if __name__ == "__main__":

    statLabels = ["Signal average: ", "Signal absolute average: ", "Signal average power: ", "Signal variance: ", "Signal RMS(root mean square): "]
    discreteFuncs = ["singlePulse", "pulseNoice"]

    choice = input(
        "Choose what to do: \
        \n1. Create signal \
        \n2.Load signal from file \
        \n3.Combine 2 signals \
        \n"
    )
    if choice == '1':
        
        choice  = input(
            "What type of signal? \
            \n1.Random noise \
            \n2.Gauss noise \
            \n3.Sinusoidal signal \
            \n4.One half-rectified sinusoidal signal \
            \n5.Half-rectified sinusoidal signal \
            \n6.Square wave signal \
            \n7.Square wave symmetrical signal \
            \n8.Triangular signal \
            \n9.Unit jump \
            \n10.Unit impulse \
            \n11.Impulse noise \
            \n"
        )
        if int(choice) > 11 or int(choice) < 1:
            print("Unsupported choice! Program will now terminate")
            exit()
        
        sampleRate = float(input("Specify the sample rate(will always be 1 for discrete signals): "))
        bins = int(input("Specify number of bins for the histogram: "))
        startTime = int(input("Specify start time: "))
        duration = int(input("Specify the duration: "))
        amp = float(input("Specify the amplitude: "))

        x = [x for x in arange(float(startTime), float(startTime+duration), sampleRate)]
        y = []
        stats = []
        args = None
        funcName = ""

        if choice == '1':
            y = graph(x, RandomNoice, (amp, ))
            graphHist(y, bins)
            stats = allStats(y)
            args = (amp, )
            funcName = RandomNoice.__name__

        elif choice == '2':
            y = graph(x, GauusNoice, (amp, ))
            graphHist(y, bins)
            stats = allStats(y)
            args = (amp, )
            funcName = GauusNoice.__name__

        elif choice == '3':
            T = float(input("Specify the cycle length: "))
            y = graph(x, SinSignal, (amp, T, startTime))
            graphHist(y, bins, T)
            stats = allStats(y, T)
            args = (amp, T, startTime)
            funcName = SinSignal.__name__

        elif choice == '4':
            T = float(input("Specify the cycle length: "))
            y = graph(x, SinSingleHalfFlatSignal, (amp, T, startTime))
            graphHist(y, bins, T)
            stats = allStats(y, T)
            args = (amp, T, startTime)
            funcName = SinSingleHalfFlatSignal.__name__

        elif choice == '5':
            T = float(input("Specify the cycle length: "))
            y = graph(x, SinDoubleHalfFlatSignal, (amp, T, startTime))
            graphHist(y, bins, T)
            stats = allStats(y, T)
            args = (amp, T, startTime)
            funcName = SinDoubleHalfFlatSignal.__name__

        elif choice == '6':
            T = float(input("Specify the cycle length: "))
            k = float(input("Specify the fill ratio: "))
            y = graph(x, RectSignal, (amp, T, startTime, k))
            graphHist(y, bins, T)
            stats = allStats(y, T)
            args = (amp, T, startTime, k)
            funcName = RectSignal.__name__

        elif choice == '7':
            T = float(input("Specify the cycle length: "))
            k = float(input("Specify the fill ratio: "))
            y = graph(x, RectSignal, (amp, T, startTime, k, 1))
            graphHist(y, bins, T)
            stats = allStats(y, T)
            args = (amp, T, startTime, k, 1)
            funcName = RectSignal.__name__

        elif choice == '8':
            T = float(input("Specify the cycle length: "))
            k = float(input("Specify the fill ratio: "))
            y = graph(x, triangleSignal, (amp, T, startTime, k))
            graphHist(y, bins, T)
            stats = allStats(y, T)
            args = (amp, T, startTime, k)
            funcName = triangleSignal.__name__

        elif choice == '9':
            jumpTime = int(input("Specify the time of signal jump: "))
            y = graph(x, unitJump, (amp, jumpTime))
            graphHist(y, bins)
            stats = allStats(y)
            args = (amp, jumpTime)
            funcName = unitJump.__name__

        elif choice == '10':
            jumpTime = int(input("Specify the time of signal pulse: "))
            x = [x for x in arange(float(startTime), float(startTime+duration), 1)]
            y = graphDis(x, singlePulse, (jumpTime, ))
            graphHist(y, bins)
            stats = allStats(y)
            args = (amp, jumpTime)
            funcName = singlePulse.__name__

        elif choice == '11':
            chance = int(input("Specify the chance of signal pulse in range (0;1]: "))
            x = [x for x in arange(float(startTime), float(startTime+duration), 1)]
            y = graphDis(x, pulseNoice, (chance, ))
            graphHist(y, bins)
            stats = allStats(y)
            args = (amp, chance)
            funcName = pulseNoice.__name__
        
        for i, val in enumerate(stats):
            print(statLabels[i] + str(val))
        print()

        choice = input("Save to file?(y/n): ")
        if choice == 'y':
            filename = input("Specify name of the file: ")
            if filename[-4] != "." : filename += ".sig"
            saveToFile(x, y, args, funcName, filename)
        else:
            print("Signal won't be saved")

        print("Program will now terminate.")
        exit()
    
    elif choice == "2":

        stats = []

        filename = input("Specify name of the file: ")
        if filename[-4] != "." : filename += ".sig"

        bins = int(input("Specify number of bins for the histogram: "))

        x, y, funcName, args = loadFromFile(filename)

        if funcName in discreteFuncs : graphDis(x, eval(funcName), args, y)
        else : graph(x, eval(funcName), args, y)

        if len(args) > 2 :
            stats = allStats(y, args[1])
            graphHist(y, bins, args[1])
        else :
            stats = allStats(y)
            graphHist(y, bins)

        for i, val in enumerate(stats):
            print(statLabels[i] + str(val))
        print("\n")

        print("Program will now terminate.")
        exit()

    elif choice == '3':

        filename1 = input("Specify name of the first file: ")
        if filename1[-4] != "." : filename1 += ".sig"
        filename2 = input("Specify name of the second file: ")
        if filename2[-4] != "." : filename2 += ".sig"

        x1, y1, funcName1, args1 = loadFromFile(filename1)
        x2, y2, funcName2, args2 = loadFromFile(filename2)

        choice = input("Choose one of the operations: \n1.Add \n2.Subtract \n3.Multiply \n4.Divide \n")
        oper = None
        if choice == '1' : oper = operator.add
        elif choice == '2' : oper = operator.sub
        elif choice == '3' : oper = operator.mul
        elif choice == '4' : oper = operator.truediv
        else:
            print("Incorrect choice, program will now terminate.")
            exit()

        resultX, resultY = signalOperation(x1, x2, y1, y2, oper)

        graphOperation(x1, x2, resultX, y1, y2, resultY)

        print("Program will now terminate.")

    else:
        print("Not a viable choice, program will now terminate.")