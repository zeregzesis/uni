import sys
import re
import os
from copy import deepcopy
from time import perf_counter_ns

recursionLimit = 20

finalBoard = []

visitedBoardStates = []

def fillFinalBoard(size):

    currentNumber = 1

    for x in range(size[0]):
        row = []

        for y in range(size[1]):
            row.append(currentNumber)
            currentNumber += 1

        finalBoard.append(row)

    finalBoard[-1][-1] = 0



def validatePath(board, move):

    for x, y in ((row, column) for row in range(len(board)) for column in range(len(board[0]))):
        if not board[x][y]:
            break
    
    if move == 'L':
        if y-1 < 0 : return None, -1
        temp = board[x][y-1]
        board[x][y-1] = 0
        board[x][y] = temp
        y -= 1
    elif move == 'R' :
        if y+1 >= len(board[0]) : return None, -1
        temp = board[x][y+1]
        board[x][y+1] = 0
        board[x][y] = temp
        y += 1
    elif move == 'U' :
        if x-1 < 0 : return None, -1
        temp = board[x-1][y]
        board[x-1][y] = 0
        board[x][y] = temp
        x -= 1
    else :
        if x+1 >= len(board) : return None, -1
        temp = board[x+1][y]
        board[x+1][y] = 0
        board[x][y] = temp
        x += 1

    if hash(str(board)) in visitedBoardStates:
        return None, -1

    visitedBoardStates.append(hash(str(board)))
    
    if not hash(str(board)) == hash(str(finalBoard)):
        return board, 0

    return board, 1




def bfs(param, puzzle):

    visitedBoardStates.append(hash(str(puzzle)))
    processedStates = 0

    # queue of paths
    paths = []
    puzzles = [deepcopy(puzzle)]

    for direction in param:   
        paths.append([direction])

    # do until there are paths to test
    while paths:

        currentPath = paths[0]
        del paths[0]

        if not processedStates % 4:
            currentPuzzle = puzzles[0]
            del puzzles[0]

        new_puzzle, validate = validatePath(deepcopy(currentPuzzle), currentPath[-1])
        processedStates += 1

        if validate == 1:
            return currentPath, processedStates, len(currentPath)
        elif validate == -1:
            continue


        for direction in param:
           paths.append(currentPath + [direction])
        puzzles.append(new_puzzle)


    # when no viable path is found
    return None, processedStates, recursionLimit
        

def dfs(param, puzzle, currentRecursion = 0, maxRecursion = 0, processedStates = 0, path = []):

    currentRecursion += 1

    if currentRecursion > maxRecursion:
        maxRecursion = recursionLimit

    if currentRecursion > recursionLimit:
        # maxRecursion = recursionLimit
        return None, processedStates, maxRecursion
    
    for direction in param:
        newPath = deepcopy(path)
        newPath.append(direction)
        new_puzzle, validate = validatePath(deepcopy(puzzle), direction)
        processedStates += 1
        if validate == 1:
            return deepcopy(newPath), processedStates, maxRecursion
        elif validate == -1:
            continue

        resultPath, processedStates, maxRecursion = dfs(param, deepcopy(new_puzzle), deepcopy(currentRecursion), maxRecursion, processedStates, deepcopy(newPath))

        if resultPath:
            return resultPath, processedStates, maxRecursion
        
    return None, processedStates, maxRecursion
    

def manh(puzzle):
    distance = 0
    current_value = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            tmp = puzzle[i][j]
            current_value += 1
            x = (tmp - 1) // len(puzzle)
            y = (tmp - 1) % len(puzzle[0])
            if tmp == 0:
                x = len(puzzle) - 1
                y = len(puzzle[0]) - 1
            distance += abs(i - x) + abs(j - y)

    return distance


def hamm(puzzle):
    distance = 0
    current_value = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            tmp = puzzle[i][j]
            current_value += 1
            if tmp == 0 and i == len(puzzle) - 1 and j == len(puzzle[0]) - 1:
                continue
            if tmp != current_value:
                distance += 1

    return distance

class Node():
    def __init__(self, puzzle, path):
        self.puzzle = puzzle
        self.path = path
        self.dist_from_start: int = 0
        self.aprox_dist_from_start: int = 0

def astr(param, puzzle):

    distance_func = manh if param == "manh" else hamm

    processedStates = 0

    state_scores = {}
    open_list: list[Node] = []
    open_list.append(Node(deepcopy(puzzle), []))

    while len(open_list) > 0:

        processedStates += 1

        current_node = open_list[0]
        for node in open_list:
            if node.aprox_dist_from_start < current_node.aprox_dist_from_start:
                current_node = node
        open_list.remove(current_node)

        if hash(str(current_node.puzzle)) == hash(str(finalBoard)):
            return current_node.path

        for direction in ['L','R','U','D']:
            new_puzzle, validate = validatePath(deepcopy(current_node.puzzle), direction)

            if validate == -1:
                continue
            elif validate == 1:
                result = deepcopy(current_node.path)
                result.append(direction)
                return result, processedStates, len(result)


            distance_from_start = current_node.dist_from_start + 1
            aprox_distance = distance_from_start + \
                distance_func(new_puzzle)

            if (hash(str(new_puzzle)) not in state_scores) or (distance_from_start < state_scores[hash(str(new_puzzle))]):

                state_scores[hash(str(new_puzzle))] = distance_from_start
                newPath = deepcopy(current_node.path)
                newPath.append(direction)
                new_node = Node(new_puzzle, newPath)
                new_node.dist_from_start = distance_from_start
                new_node.aprox_dist_from_start = aprox_distance
                open_list.append(new_node)

'''

puzzleHandle = open("C:\\Users\\maste\\Desktop\\other\\SISE_15\\puzzles\\4x4_07_00008.txt")
gameSize = [int(x) for x in puzzleHandle.readline().split()]
gameFrame = [[int(x) for x in line.split()] for line in puzzleHandle]

fillFinalBoard(gameSize)

# visitedBoardStates.append(hash(str(gameFrame)))
print(dfs("LUDR", gameFrame))
#'''
#'''
if __name__ == '__main__':

    strategy = sys.argv[1]
    param = sys.argv[2]
    puzzleFile = sys.argv[3]
    solutionFile = sys.argv[4]
    statisticsFile = sys.argv[5]
    
    '''
    strategy = 'dfs'
    param = "RDUL"
    puzzleFile = "4x4_07_00008.txt"
    solutionFile = "4x4_07_0008_dfs_LUDR_sol.txt"
    statisticsFile = "4x4_07_0008_dfs_LUDR_stats.txt"
    '''
    

    if strategy not in ['bfs', 'dfs', 'astr']:
        raise Exception("Unknown strategy given.")

    if strategy == 'astr' and param not in ['hamm', 'manh']:
        raise Exception("Unknown heuristic for A* strategy given.")

    # elif not (re.match(r'^(?=.*R)(?=.*U)(?=.*L)(?=.*D).*$', param) and len(param) == 4):
        # raise Exception("Unknown search order given.")

    # create directories if they don't exist
    if not os.path.exists("solutions") : os.mkdir("solutions")
    if not os.path.exists("solutions/" + strategy) : os.mkdir("solutions/" + strategy)
    if not os.path.exists("solutions/" + strategy + "/" + param) : os.mkdir("solutions/" + strategy + "/" + param)

    if not os.path.exists("statistics") : os.mkdir("statistics")
    if not os.path.exists("statistics/" + strategy) : os.mkdir("statistics/" + strategy)
    if not os.path.exists("statistics/" + strategy + "/" + param) : os.mkdir("statistics/" + strategy + "/" + param)

    path = None
    processedStates = None
    maxDepth = None

    puzzleFile = "C:\\Users\\maste\\Desktop\\other\\SISE_15\\puzzles\\" + puzzleFile

    puzzleHandle = open(puzzleFile)
    gameSize = [int(x) for x in puzzleHandle.readline().split()]
    gameFrame = [[int(x) for x in line.split()] for line in puzzleHandle]

    fillFinalBoard(gameSize)

    if strategy == "bfs":
        startTime = perf_counter_ns()
        path, processedStates, maxDepth = bfs(param, gameFrame)
        finalTime = (perf_counter_ns() - startTime) / 1000000
    elif strategy == "dfs" :
        visitedBoardStates.append(hash(str(gameFrame)))
        startTime = perf_counter_ns()
        path, processedStates, maxDepth = dfs(param, gameFrame)
        finalTime = (perf_counter_ns() - startTime) / 1000000
    else:
        startTime = perf_counter_ns()
        path, processedStates, maxDepth = astr(param, gameFrame)
        finalTime = (perf_counter_ns() - startTime) / 1000000



    # startTime = perf_counter()
    # exec("path, processedStates, maxDepth = " +  strategy + "(param, gameFrame)")
    # finalTime = (perf_counter() - startTime) / 1000000

    visitedStates = len(visitedBoardStates)
    solutionLength = len(path) if path else -1

    f = open("solutions/" + strategy + "/" + param + "/" + solutionFile, 'w')
    if path:
        f.write(str(solutionLength) + "\n" + ''.join(path))
    else:
        f.write(str(solutionLength))
    f.close()

    f = open("statistics/" + strategy + "/" + param + "/" + statisticsFile, 'w')
    if path:
        f.write(str(solutionLength) + "\n" + str(visitedStates) + "\n" + str(processedStates) + "\n" + str(maxDepth) + "\n" + str(round(finalTime, 3)))
    else:
        f.write(str(solutionLength) + "\n" + str(visitedStates) + "\n" + str(processedStates) + "\n" + str(maxDepth) + "\n" + str(round(finalTime, 3)))
    f.close()

#'''