from functions import *
import time

def inputNodes():
    startNode = int(input("Type start node: "))
    endNode = int(input("Type end node: "))
    return startNode, endNode

if __name__ == '__main__':
    print("Choose graph representation:")
    print("1. Array (tablica)")
    print("2. Adjacency matrix (macierz sasiedztwa)")
    print("3. Incidence Matrix (macierz incydencji)")
    print("4. Adjacency list (lista sasiedztwa)")
    graphChoice = int(input("Your choice: "))
    ifDirected = int(input("Does the graph have to be directed (type 1) or not (type 0)?"))
    print("Choose graph search method")
    print("0. Breath-First-Search (Przeszukiwanie w wszerz)")
    print("1. Depth-First-Search (Przeszukiwanie w glab")
    methodChoice = int(input("Your choice: "))

    if graphChoice in range(1,5) and ifDirected in range(0,2) and methodChoice in range(0,2):
        if graphChoice == 1:
            graph = constructTable(ifDirected)
            startNode, endNode = inputNodes()
            timeStart = time.perf_counter()
            result = searchArray(startNode, endNode, graph, ifDirected, methodChoice)
            timeEnd = time.perf_counter()
            
        elif graphChoice == 2:
            graph = constructMatrixA(ifDirected)
            startNode, endNode = inputNodes()
            timeStart = time.perf_counter()
            result = searchMatrixA(startNode, endNode, graph, methodChoice)
            timeEnd = time.perf_counter()

        elif graphChoice == 3:
            graph = constructMatrixI(ifDirected)
            startNode, endNode = inputNodes()
            timeStart = time.perf_counter()
            result = searchMatrixI(startNode, endNode, graph, methodChoice)
            timeEnd = time.perf_counter()

        elif graphChoice == 4:
            graph = constructListA()
            startNode, endNode = inputNodes()
            timeStart = time.perf_counter()
            result = searchListA(startNode, endNode, graph, methodChoice)
            timeEnd = time.perf_counter()
        
    print("The path from the start node to the end node: ", result)
    print(f"Search time: {timeEnd - timeStart:0.6f}")