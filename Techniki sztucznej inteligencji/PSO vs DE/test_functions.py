import math

def f2(argTab):
    total = 0
    for i, arg in enumerate(argTab):
        total += pow(arg - (i+1), 2)
    return total

def rastrigin(argTab):
    total =0
    for i, arg in enumerate(argTab):
        total+=pow(arg, 2)-10*math.cos(2*math.pi*arg)+10
    return total