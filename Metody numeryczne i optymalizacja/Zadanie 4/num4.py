from numpy import sin, cos, sqrt, exp
from sympy import *
from math import factorial, log
from scipy.misc import derivative
from sympy.utilities.lambdify import lambdastr
import matplotlib.pyplot as plt
import numpy as np

def wzor(x0, x1, x2, h, func):
    x = x0
    y0 = eval(func)
    x = x1
    y1 = eval(func)
    x = x2
    y2 = eval(func)
    return h/3 * (y0 + 4*y1 + y2)



def calkaNewtonaCotesa(x0, x2, func, prec):

    h = abs(x2 - x0) * 0.5

    x1 = x0 + h

    if not h == abs(x1 - x0):
        return None
    
    prev = wzor(x0, x1, x2, h, func)
    currentPrec = 100

    counter = 2
    current = 0
    while prec < currentPrec:
        h -= h/counter
        xStart = x0
        current = 0
        points = []
        for _ in range(counter):
            xMid = xStart + h
            xEnd = xMid + h
            points.append(xStart)
            points.append(xMid)
            current += wzor(xStart, xMid, xEnd, h, func)
            xStart = xEnd

        currentPrec = abs(current - prev)
        prev = current
        counter += 1
    points.append(xEnd)
    return current, points



def ncIfn(func, precLim, prec, interval):
    func = 'exp(-x) * ' + func
    begin = 0
    end = 0 + interval
    agregate = 0
    points = []
    current, point = calkaNewtonaCotesa(begin, end, func, prec)
    points += point
    while current > precLim:
        agregate += current
        begin = end
        end += interval
        current, point = calkaNewtonaCotesa(begin, end, func, prec)
        points += point

    return agregate, points


def getNodes(func):
    res = solve(func)
    resTab = []
    for num in res:
        resTab.append(re(N(eval(str(num)))))
    resTab.sort()
    return resTab

def deriv(func, x):
    return derivative(func, x, 0.0001, 1)

def calkaGaussaLaguerrea(func, nodeCount, polys):

    res = 0
    pts = []
    nodes = getNodes(polys[nodeCount+1])

    for i in range(nodeCount+1):

        temp = 0
        x = symbols('x')

        fac = factorial(nodeCount+1)
        fac *= fac
        l1 = lambdify(x, polys[nodeCount+1])        # l1 = lambda x : polys[nodeCount+1]
        der = deriv(l1, nodes[i])
        l2 = lambdify(x, polys[nodeCount+2])        # l2 = lambda x : polys[nodeCount+2]
        l2val = l2(nodes[i])
        
        temp += -1 * (fac / (der * l2val))
        x = nodes[i]
        temp *= eval(func)
        pts.append(temp)

        res += temp

    return res, nodes, pts


def plotCompare(xTab, lab, func, val):

    newY = []
    bars = [2 * xTab[0]]
    for i in range(len(xTab)):
        x = xTab[i]
        newY.append(eval(func))
        if not i == 0:
            bars.append(2 * abs(xTab[i] - sum(bars[:i])))

    plt.plot([], [], ' ', label="Wyliczona wartość całki: " + str(float(val)))

    plt.bar(xTab, newY, width=bars, alpha=0.4, align='center', edgecolor='black', color='green', label=lab)

    xTabNew = np.arange(0, xTab[-1], 0.1)
    yTab = []
    for i in range(len(xTabNew)):
        x = xTabNew[i]
        yTab.append(eval(func))

    plt.plot(xTabNew, yTab, label='Całkowana funkcja')

    plt.ylabel(func)
    plt.legend()
    plt.show()