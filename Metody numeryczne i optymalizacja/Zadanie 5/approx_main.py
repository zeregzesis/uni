from approx_func import *

if __name__ == '__main__':

    
    func = input("Podaj oryginalną funkcję: ")
    start = -1
    while start < 0: start = float(input("Podaj początek przedziału(minimum 0): "))
    stop = float(input("Podaj koniec przedziału: "))
    prec = float(input("Podaj oczekowaną precyzję(jeśli bez precyzji wpisz -1): "))

    if prec < 0:

        n = int(input("Podaj stopień wielomianu aproksymującego: "))
        m = int(input("Podaj stopień kwadratury: "))

        coeffs = getCoeffs(func, n, m)

        approxPoly = getApprox(coeffs)
        print(approxPoly)

        func = lambdify(symbols('x'), func)

        approxFunc = lambdify(symbols('x'), approxPoly)

        graph(func, approxFunc, start, stop)

    else:
        f = lambdify(symbols('x'), func)
        n = 2
        m = 2

        coeffs = getCoeffs(func, n, m)
        approxPoly = getApprox(coeffs)
        approxFunc = lambdify(symbols('x'), approxPoly)
        xTab = arange(start, stop, 0.1)
        yTab = array([])
        for x in xTab:
            yTab = append(yTab, func(x)) 
        yTabNew = array([])
        for x in xTab:
            yTabNew = append(yTabNew, approx(x))
        minErr = getErr(yTab, yTabNew)
        lastErr = minErr

        while minErr > prec:

            coeffs = getCoeffs(func, n, m)
            approxPoly = getApprox(coeffs)
            approxFunc = lambdify(symbols('x'), approxPoly)

            yTab = array([])
            for x in xTab:
                yTab = append(yTab, func(x)) 

            yTabNew = array([])
            for x in xTab:
                yTabNew = append(yTabNew, approxFunc(x))
            curErr = getErr(yTab, yTabNew)

            if curErr <= minErr:
                minErr = curErr
                m += 1
                continue

            if curErr > minErr:
                n += 1
                if n > 16:
                    print("Żądana precyzja niemożliwa dla zadanej funkcji")
                    exit(1)

        graph(f, approxFunc, start, stop)