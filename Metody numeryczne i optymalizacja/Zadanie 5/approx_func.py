from numpy import exp, sin, cos, arange, array, append
from sympy import *
from scipy.special import genlaguerre, roots_genlaguerre
import matplotlib.pyplot as plt
import re

def cGL(func, n):

    res = 0
    roots = roots_genlaguerre(n, 0)
    nodes = roots[0]
    weights = roots[1]

    for i in range(n):
        temp = func(nodes[i]) * weights[i]
        res += temp

    return res

def laguerrePoly(deg):

    if deg == 0: return "1"
    if deg == 1: return "x-1"

    x = symbols('x')
    temp = "x**" + str(deg) + "*exp(-x)"

    toDer = diff(temp)

    for j in range(1,deg):
        toDer = diff(toDer)

    if not deg % 2 == 0:
        toDer *= -1

    toDer = simplify(toDer * exp(x))

    return str(toDer)

def getErr(yTab, yTabNew):
    err = 0

    for i in range(len(yTab)):
        err += abs(yTab[i] - yTabNew[i])

    return err / len(yTab)

def graph(func, approx, start, stop):

    xTab = arange(start, stop, 0.1)
    yTab = array([])

    for x in xTab:
        yTab = append(yTab, func(x)) 
    
    yTabNew = array([])

    for x in xTab:
       yTabNew = append(yTabNew, approx(x))
    
    err = round(getErr(yTab, yTabNew), 5)

    plt.plot(xTab, yTab, color='red', label='Oryginalna funkcja')
    plt.plot(xTab, yTabNew, color='green', label='Aproksymacja', alpha=0.5)
    plt.plot([],[], label='Błąd aproksymacji = ' + str(err))
    plt.legend()
    plt.show()

def getCoeffs(func, n, m):

    coeffs = []

    for i in range(n+1):
        f1 = lambdify(symbols('x'), "(" + func + ") * (" + laguerrePoly(i) + ")")
        f2 = lambdify(symbols('x'), "(" + laguerrePoly(i) + ") * (" +  laguerrePoly(i) + ")")
        coeffs.append(round(cGL(f1, m), 5) / cGL(f2, m))

    return coeffs

def getApprox(coeffs):

    res = ''
    for i in range(len(coeffs)):
        res += str(coeffs[i]) + " * (" + laguerrePoly(i) + ") + "

    res = res[:-2]

    ret = simplify(res)

    return toHorner(str(ret))

def toHorner(eq):

    temp = re.sub(r'\*{1}[x]{1}\**[0-9]*', ')*x', eq)

    for i in range(temp.count('x')):
        temp = "(" + temp

    return temp