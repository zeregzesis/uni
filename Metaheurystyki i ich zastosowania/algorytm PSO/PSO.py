from math import floor, sin, sqrt, inf
from random import uniform
from matplotlib.pyplot import show, scatter

def swarmStateGraph(swarm, currentBest):

    scatter([e.pos[0] for e in swarm], [e.pos[1] for e in swarm], color='blue')

    scatter(currentBest.pos[0], currentBest.pos[1], color='red')

    show()

def addTuple(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]

class Particle:

    def __init__(self, min, max, func):
        self.min = min
        self.max = max
        self.func = func
        self.pos = uniform(min,max), uniform(min, max)
        self.bestPos = self.pos
        self.vel = 0, 0
        self.getValue()
    
    def getValue(self):
        self.value = self.func(self.pos[0], self.pos[1])
        if self.value < self.func(self.bestPos[0], self.bestPos[1]):
            self.bestPos = self.pos
        return self.value

    def rebound(self):
        self.pos = max(min(self.pos[0], self.max), self.min), max(min(self.pos[1], self.max), self.min)

    def getBestValue(self):
        return self.func(self.bestPos[0], self.bestPos[1])


# Booth function
'''
func = lambda x, y: (x + 2*y -7)**2 + (2*x + y - 5)**2
minVal = -10
maxVal = 10
best = 0.0
'''

# Eggholder function
'''
func = lambda x, y : -(y + 47) * sin(sqrt(abs((x/2)+(y+47)))) - x * sin(sqrt(abs(x-(y+47))))
minVal = -512
maxVal = 512
best = -959.6407
'''

# Beale function
func = lambda x, y : (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2
minVal = -4.5
maxVal = 4.5
best = 0.0

swarm = []
popsize = 50
swarmBest = inf

inertiaWeight = 0.8
cognitiveCoeff = 1.45
socialCoeff = 2.65

temp = cognitiveCoeff + socialCoeff

constriction = 2 / abs(2 - temp - sqrt(temp**2 - 4*temp))

counter = 0

if __name__ == '__main__':

    for i in range(popsize):
        particle = Particle(minVal, maxVal, func)
        swarm.append(particle)
    currentBest = sorted(swarm, key=lambda x: x.getBestValue())[0]

    print(currentBest.getBestValue())

    swarmStateGraph(swarm, currentBest)

    while counter < 10000:
        for particle in swarm:
            newVel = ()
            for d in range(len(particle.pos)):
                rp = uniform(0,1)
                rg = uniform(0,1)

                newVel += (inertiaWeight * particle.vel[d] + cognitiveCoeff * rp * (particle.bestPos[d] - particle.pos[d]) + socialCoeff * rg * (currentBest.bestPos[d] - particle.pos[d]), )
                # newVel += (inertiaWeight * particle.pos[d] + cognitiveCoeff * rp * (particle.bestPos[d] - particle.pos[d]) + socialCoeff * rg * (currentBest.bestPos[d] - particle.pos[d]), )
            particle.vel = newVel
            particle.pos = addTuple(particle.pos, particle.vel)
            particle.rebound()
            particle.getValue()
        currentBest = sorted(swarm, key=lambda x: x.getValue())[0]
        print(currentBest.getValue())
        inertiaWeight = 0.8 - (((0.8 - 0.1) / 10000) * counter)
        # swarmStateGraph(swarm, currentBest)
        if not counter % 1000 : swarmStateGraph(swarm, currentBest)
        counter += 1