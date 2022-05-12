from defs import *

class Test():

    def __init__(self, value):
        self.value = value

a = [Test(2) for x in range(3)]

for x in r.sample(a,2):
    x.value = 3

for x in a:
    print(x.value)