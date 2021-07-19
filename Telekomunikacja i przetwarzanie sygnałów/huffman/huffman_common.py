import numpy as np
from itertools import chain
import pickle
import socket
import struct
from bitstring import ConstBitStream
import math
import bitstring as bs

class node:
    def __init__(self, charCount, char, left=None, right=None):
        self.charCount = charCount
        self.char = char
        self.left = left
        self.right = right
        self.huff = ''

def printNodes(node, val=''):

    newVal = val + str(node.huff)

    if(node.left):
        printNodes(node.left, newVal)

    if(node.right):
        printNodes(node.right, newVal)
 
    if(not node.left and not node.right):
        print(f"{node.char} -> {newVal}")