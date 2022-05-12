import numpy as np

##############################################################################################################

def promptPairs(directed):
    """
    Prompt for constructing array and matrices; returns number of nodes of the graph to be created.
        Input:
            directed -- Flag to display prompt regarding directed graphs.
        Output:
            < int >
    """

    nodeCount = int(input("Input number of nodes: "))
    print("Input pairs of nodes")

    if directed:
        print("First node is source, second is target")
    
    return nodeCount

##############################################################################################################

def constructTable(directed):
    """
    Creates table of tuples representing connected nodes. First value is source in case of directed graph.
        Input:
            directed -- Flag to display prompt regarding directed graphs.
        Output:
            < List < Tuple < (int, int) > > >
    """

    nodeCount = promptPairs(directed)
    tab = []

    # get tuple representing connection between nodes; if nothing is passed, end function
    try:
        x = tuple(map(int, input().split(',')))
    except:
        return

    # condition to ensure no 'out-of-range' connections
    while (x[0] <= nodeCount and x[1] <= nodeCount):

        # node can't be connected to itself and connection must be new
        if(x[0] != x[1] and x not in tab and x[::-1] not in tab):
            tab.append(x)

        # if nothing is given as input, break 'while' loop
        try:
            x = tuple(map(int, input().split(',')))
        except:
            break
    
    return tab

##############################################################################################################

def constructMatrixA(directed):
    """
    Creates adjacency matrix, representing neighbouring nodes.
        Input:
            directed -- Flag to display prompt regarding directed graphs.
        Output:
            < List < List < int > > >
    """

    nodeCount = promptPairs(directed)
    matrix = np.zeros((nodeCount, nodeCount))

    # get tuple representing connection between nodes; if nothing is passed, end function
    try:
        x = tuple(map(int, input().split(',')))
    except:
        return

    # condition to ensure no 'out-of-range' connections
    while (x[0] <= nodeCount and x[1] <= nodeCount):

        # node can't be connected to itself
        if(x[0] != x[1]):
            matrix[ x[0]-1 ][ x[1]-1 ] = 1
            if not directed:
                matrix[ x[1]-1 ][ x[0]-1 ] = 1

        # if nothing is given as input, break 'while' loop
        try:
            x = tuple(map(int, input().split(',')))
        except:
            break
    
    return matrix

##############################################################################################################

def constructMatrixI(directed):
    """
    Creates incidence matrix representing connections betweeen nodes.
        Input:
            directed -- Flag to display prompt regarding directed graphs.
        Output:
            < List < List < int > > >
    """

    nodeCount = promptPairs(directed)
    matrix = []

    # get tuple representing connection between nodes; if nothing is passed, end function
    try:
        x = tuple(map(int, input().split(',')))
    except:
        return

    # condition to ensure no 'out-of-range' connections
    while (x[0] <= nodeCount and x[1] <= nodeCount):

        # node can't be connected to itself
        if(x[0] != x[1]):

            # create vector representing the connection
            temp = [0 for x in range(nodeCount)]

            # if graph is directed, mark source node differently than destination
            if directed:
                temp[ x[0]-1 ] = 2
            else:
                temp[ x[0]-1 ] = 1
            temp[ x[1]-1 ] = 1

            # connection must be new
            if(temp not in matrix):
                matrix.append(temp)

        # if nothing is given as input, break 'while' loop
        try:
            x = tuple(map(int, input().split(',')))
        except:
            break

    return matrix

##############################################################################################################

def verifySubList(nodeCount, currentNode, subList):
    """
    Verifies user input for creating adjacency list.
        Input:
            nodeCount       -- Number of nodes of the graph.
             currentNode    -- Node for which the sublist gives connections to.
            subList         -- Sublist to verify.
        Output:
            None    -- Sublist is invalid.
             1      -- Sublist is valid.
    """

    # check if node connects to itself or nonexistent node was given or any duplicate nodes were passed
    if any(i == currentNode for i in subList) or any(i > nodeCount for i in subList) or len(subList) != len(set(subList)):
        return None
    return 1

##############################################################################################################

def constructListA():
    """
    Creates adjacency list that represents connections a nodes have with other nodes.
        Input:
            None
        Output:
            < List < List < int > > >
    """

    nodeCount = int(input("Input number of nodes: "))

    currentNode = 1
    listN = list([])

    # prompt to make sure correct graph is created
    print("\nCurrent node is the source, if you want indirected graph, indicate connection for both nodes\n")

    # condition to ensure all nodes are given their connections
    while (currentNode <= nodeCount):

        print("Input nodes that node " + str(currentNode) + " connects to: ")

        # get list representing connections to current node; if nothing is passed, retry
        try:
            x = list(map(int, input().split(',')))
        except:
            x = []

        # verivy sublist, retry if invalid
        if(verifySubList(nodeCount, currentNode, x)):
            listN.append(x)
        else:
            print("Incorrect list of connections given")
            continue

        # move to next node
        currentNode += 1
    
    return listN

##############################################################################################################

def searchArray(startNode, endNode, graph, directed, mode):
    """
    Performs search for array graph.
        Input:
            startNode   -- Node from which to begin the search.
             endNode    -- Node to which path must be found.
            graph       -- Graph in which to look for the path.
             directed   -- Flag to indicate whether the graph is directed or indirected.
            mode        -- 0 if breath-first search, 1 if depth-first.
        Output:
            None                -- Path not found.
             < List < int > >   -- Path is found.
    """
    
    # queue of paths
    paths = [[startNode]]

    visited = []

    # do until there are paths to test
    while paths:

        if mode == 0:
            currentPath = paths[0]
            del paths[0]
        else:
            currentPath = paths.pop()

        # abandon paths that return to already visited nodes
        if currentPath[-1] not in visited:
            visited.append(currentPath[-1])
        else:
            continue

        #condition if path to target is found
        if currentPath[-1] == endNode:
            return currentPath

        # if graph is directed, only one-way connections are considered
        if directed:

            for x in graph:
                if x[0] == currentPath[-1]:
                    paths.append( currentPath + [x[1]] )

        # if graph is not directed, both ways must be considered
        else:
            for x in graph:
                if x[0] == currentPath[-1]:
                    paths.append( currentPath + [x[1]] )
                if x[1] == currentPath[-1]:
                    paths.append( currentPath + [x[0]] )

    # when no viable path is found
    return None

##############################################################################################################

def searchMatrixA(startNode, endNode, graph, mode):
    """
    Performs search for adjacency matrix graph.
        Input:
            startNode   -- Node from which to begin the search.
             endNode    -- Node to which path must be found.
            graph       -- Graph in which to look for the path.
             mode        -- 0 if breath-first search, 1 if depth-first.
        Output:
            None                -- Path not found.
             < List < int > >   -- Path is found.
    """
    
    # queue of paths
    paths = [[startNode]]

    visited = []

    # do until there are paths to test
    while paths:

        if mode == 0:
            currentPath = paths[0]
            del paths[0]
        else:
            currentPath = paths.pop()
        
        # abandon paths that return to already visited nodes
        if currentPath[-1] not in visited:
            visited.append(currentPath[-1])
        else:
            continue

        #condition if path to target is found
        if currentPath[-1] == endNode:
            return currentPath

        # look if given node has connection to others; directionality handled by correct construction of graph
        elemNum = 1
        for x in graph[currentPath[-1]-1]:
            if x == 1:
                paths.append( currentPath + [elemNum] )
            elemNum += 1

    # when no viable path is found
    return None

##############################################################################################################

def searchMatrixI(startNode, endNode, graph, mode):
    """
    Performs search for incidence matrix graph.
        Input:
            startNode   -- Node from which to begin the search.
             endNode    -- Node to which path must be found.
            graph       -- Graph in which to look for the path.
             mode        -- 0 if breath-first search, 1 if depth-first.
        Output:
            None                -- Path not found.
             < List < int > >   -- Path is found.
    """
    
    # queue of paths
    paths = [[startNode]]
    visited = []

    # do until there are paths to test
    while paths:

        if mode == 0:
            currentPath = paths[0]
            del paths[0]
        else:
            currentPath = paths.pop()

        # abandon paths that return to already visited nodes
        if currentPath[-1] not in visited:
            visited.append(currentPath[-1])
        else:
            continue

        #condition if path to target is found
        if currentPath[-1] == endNode:
            return currentPath

        for row in graph:
            # in case of indirected graph
            if(row.count(1) == 2):
                if row[currentPath[-1]-1] == 1:

                    # in case current node number is smaller than the node it connects to
                    if row.index(1) + 1 == currentPath[-1]:
                        paths.append( currentPath + [ row[row.index(1)+1:].index(1) + row.index(1) + 2 ])
                    else:
                        paths.append( currentPath + [row.index(1)+1] )
            
            # in case of directed graph
            else:
                if row[currentPath[-1]-1] == 2:
                    paths.append( currentPath + [row.index(1)+1] )

    # when no viable path is found
    return None

##############################################################################################################

def searchListA(startNode, endNode, graph, mode):
    """
    Performs search for adjacency list graph.
        Input:
            startNode   -- Node from which to begin the search.
             endNode    -- Node to which path must be found.
            graph       -- Graph in which to look for the path.
             mode        -- 0 if breath-first search, 1 if depth-first.
        Output:
            None                -- Path not found.
             < List < int > >   -- Path is found.
    """
    
    # queue of paths
    paths = [[startNode]]

    visited = []

    # do until there are paths to test
    while paths:

        if mode == 0:
            currentPath = paths[0]
            del paths[0]
        else:
            currentPath = paths.pop()

        # abandon paths that return to already visited nodes
        if currentPath[-1] not in visited:
            visited.append(currentPath[-1])
        else:
            continue

        #condition if path to target is found
        if currentPath[-1] == endNode:
            return currentPath

        # add paths according to current node's neighbours
        for x in graph[currentPath[-1]-1]:
            paths.append( currentPath + [x] )

    # when no viable path is found
    return None

##############################################################################################################
