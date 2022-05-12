import operator
from numpy import arange
from signalSampling import *
from signalGenerator import *

if __name__ == "__main__":

    statLabels = ["Signal average: ", "Signal absolute average: ", "Signal average power: ", "Signal variance: ", "Signal RMS(root mean square): "]
    discreteFuncs = ["singlePulse", "pulseNoice"]

    choice = input(
        "Choose what to do: \
        \n1. Create signal \
        \n2.Load signal from file \
        \n3.Combine 2 signals \
        \n4. Sample and reconstruct signal \
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
            if filename[-4:] != ".sig" : filename += ".sig"
            saveToFile(x, y, args, funcName, filename)
        else:
            print("Signal won't be saved")

        print("Program will now terminate.")
        exit()
    
    elif choice == "2":

        stats = []

        filename = input("Specify name of the file: ")
        if filename[-4:] != ".sig" : filename += ".sig"

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
        if filename1[-4:] != ".sig" : filename1 += ".sig"
        filename2 = input("Specify name of the second file: ")
        if filename2[-4:] != ".sig" : filename2 += ".sig"

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

        if input("Save to file?(y/n): ") == 'y':
            filename = input("Specify name of the file: ")
            if filename[-4:] != ".sig" : filename += ".sig"
            saveToFile(resultX, resultY, None, None, filename)

        print("Program will now terminate.")


    elif choice == '4':

        complexX = None
        complexY = None
        sampleRate = None
        startTime = None
        duration = None
        amp = None
        filename = None

        operChoice = input(
            "Choose one of the operations: \
                \n1.Just sample \
                \n2.Quantization with cut \
                \n3.Quantization with rounding \
                \n4.Zero-order hold \
                \n5. First-order hold\
                \n6. Sinc interpolation\
                \n"
        )

        plot = input("Plot the result?(y/n): ")

        if input("Load signal from file?(y/n)") == 'y':

            filename = input("Specify name of the file: ")
            if filename[-4:] != ".sig" : filename += ".sig"
            complexX, complexY, func, args = loadFromFile(filename)
            sampleRate = float(input("Specify the sample rate as proportion of original samples([0;1]): "))
            xSample, ySample = sampleComplex(complexX, complexY, sampleRate)

        else:
            choice  = input(
                "Choose function representing original signal: \
                \n1.Random noise \
                \n2.Gauss noise \
                \n3.Sinusoidal signal \
                \n4.One half-rectified sinusoidal signal \
                \n5.Half-rectified sinusoidal signal \
                \n6.Square wave signal \
                \n7.Square wave symmetrical signal \
                \n8.Triangular signal \
                \n"
            )
            if int(choice) > 8 or int(choice) < 1:
                print("Unsupported choice! Program will now terminate")
                exit()
            
            sampleRate = float(input("Specify the sample rate: "))
            startTime = int(input("Specify start time: "))
            duration = int(input("Specify the duration: "))
            amp = float(input("Specify the amplitude: "))

            x = [x for x in arange(float(startTime), float(startTime+duration), sampleRate)]
            y = []
            stats = []
            args = None
            func = None

            if choice == '1':
                args = (amp, )
                func = RandomNoice

            elif choice == '2':
                y = graph(x, GauusNoice, (amp, ))
                stats = allStats(y)
                args = (amp, )
                func = GauusNoice

            elif choice == '3':
                T = float(input("Specify the cycle length: "))
                args = (amp, T, startTime)
                func = SinSignal

            elif choice == '4':
                T = float(input("Specify the cycle length: "))
                args = (amp, T, startTime)
                func = SinSingleHalfFlatSignal

            elif choice == '5':
                T = float(input("Specify the cycle length: "))
                args = (amp, T, startTime)
                func = SinDoubleHalfFlatSignal

            elif choice == '6':
                T = float(input("Specify the cycle length: "))
                k = float(input("Specify the fill ratio: "))
                args = (amp, T, startTime, k)
                func = RectSignal

            elif choice == '7':
                T = float(input("Specify the cycle length: "))
                k = float(input("Specify the fill ratio: "))
                args = (amp, T, startTime, k, 1)
                func = RectSignal

            elif choice == '8':
                T = float(input("Specify the cycle length: "))
                k = float(input("Specify the fill ratio: "))
                args = (amp, T, startTime, k)
                func = triangleSignal

            if int(choice) > 6 or int(choice) < 1:
                print("Unsupported choice! Program will now terminate")
                exit()

            xSample, ySample = sampleSignal(func, args, 10, sampleRate, duration)

        if operChoice == '1':
            res = sampleSignal(func, args, 10, sampleRate, duration, True if plot == 'y' else False) if not filename else sampleComplex(complexX, complexY, sampleRate, True if plot == 'y' else False)
        elif operChoice == '2':
            roundRes = float(input("Specify the quantization resolution: "))
            res = quantNoRound(xSample, ySample, roundRes, 10, sampleRate, duration, func, args, complexX, complexY, True if plot == 'y' else False)
        elif operChoice == '3':
            roundRes = float(input("Specify the quantization resolution: "))
            res = quantRound(xSample, ySample, roundRes, 10, sampleRate, duration, func, args, complexX, complexY, True if plot == 'y' else False)
        elif operChoice == '4':
            res = zeroOrderExtrapolation(xSample, ySample, 10, sampleRate, duration, func, args, complexX, complexY, True if plot == 'y' else False)
        elif operChoice == '5':
            res = firstOrderInterpolation(xSample, ySample, 10, sampleRate, duration, func, args, complexX, complexY, True if plot == 'y' else False)
        elif operChoice == '6':
            res = sincInterpolation(xSample, ySample, 10, sampleRate, duration, func, args, complexX, complexY, True if plot == 'y' else False)

        if operChoice != '1' : print(getAllMetrics(sampleSignal(func, args, 10, sampleRate * 10, duration)[1] if not filename else complexY, res))

    else:
        print("Not a viable choice, program will now terminate.")