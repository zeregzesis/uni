import numpy as np
import matplotlib.pyplot as plt


def fixMatrix(matrix, resVec):
    """Próba 'naprawy' macierzy która nie jest dominująca przekątniowo

    Argumenty:
        matrix - macierz do poprawy
        resVec = wektor wyników równań

    Zwraca:
        'None, None' jeśli przekazana macierz jest już przekątniowo dominująca lub nie da jej się w ten sposób poprawić
        W pozostałych przypadkach, poprawione macierze współczynników i wyników
    """
    a = abs(matrix)
    res = np.argmax(a, axis=1)

    # spełnienie tego warunku oznacza, że macierzy nie da się już "bardziej naprawić"
    if np.all(res == np.arange(len(matrix))):
        return None, None

    # sprawdzenie, czy nie ma duplikatów
    # jeśli ten warunek jest spełniony, nie da się naprawić macierzy
    # ponieważ nigdy nie będzie dominująca przekątniowo
    if not len(res) == len(set(res)):
        return None, None
    
    # dla każdego rzędu zamień go z rzędem, gdzie jego maks znajduje się na przekątnej
    # w ten sposób w wyniku przekształceń powstanie macierz potencjalnie przekątniowo dominująca
    # jeśli taka macierz nie spełnia warunku, nie da się jej przekaształcić tak, aby spełniała
    for i in range(len(res)):
        if res[i] == i:
            continue
        temp = np.where(res == i)[0][0]
        matrix[[i, temp]] = matrix[[temp, i]]
        resVec[i], resVec[temp] = resVec[temp], resVec[i]
        res = np.argmax(abs(matrix), axis=1)
    
    return matrix, resVec

def checkAbs(eq):
    """Sprawdzenie, czy moduł liczb na przekątnej jest większy niż suma modułów pozostałych liczb w danym rzędzie

    Argumenty:
        eq - macierz do sprawdzenia

    Zwraca:
        Wartość True jeśli testowany warunek jest spełniony, False jeśli nie
    """
    i = 0
    elemSum = 0
    for row in eq:
        for j in range(0,len(row)):
            elemSum += abs(row[j])
        elemSum -= abs(row[i])
        if(abs(row[i]) < elemSum):
            return False
        elemSum = 0
        i += 1
    return True

def checkMatrix(eq):
    """Sprawdzenie przekątniowej dominacji macierzy

    Argumenty:
        eq - macierz do sprawdzenia

    Zwraca:
        Wartość True jeśli testowany warunek jest spełniony, False jeśli nie
    """
    if(checkAbs(eq) and checkAbs(np.transpose(eq))):    # przekazując transponowaną macierz do funkcji
        return True                                     # sprawdzającej rzędy da sprawdzenie dla kolumn
    return False

def findResults(eq, res, iter, prec, exp=None):
    """Szukanie rozwiązań dla podanego układu

    Argumenty:
        eq - macierz współczynników układu równań
        res - wektor rozwiązań równań
        iter - liczba iteracji, jeśli metoda wykonywana dla precyzji, wartość ta powinna wynosić -1
        prec - oczekiwana precyzja, jeśli metoda wykonywana dla iteracji, wartość powinna wynosić 0
        exp - (opcjonalny argument) oczekiwane wyniki, potrzebne do wykresu zbieżności precyzji

    Zwraca:
        Wektor rozwiązań układu równań
    """

    #potrzebne parametry
    resVectorPrev = np.zeros(len(res))
    resVectorCurrent = np.zeros(len(res))
    L = np.tril(eq, -1)
    U = np.triu(eq, 1)
    N = np.diag(np.power(np.diag(eq), -1))
    M = np.matmul(-N,np.add(L,U))       # można zwykły operator
    change = 1

    #setup dla wykresów, działają tylko dla układu 4x4
    '''
    orgIter = iter
    yGraph = [[0],[0],[0],[0]]
    changeGraph = []
    '''

    #główna pętla
    while iter != 0 and change > prec:
        for i in range(len(res)):
            resVectorCurrent[i] = res[i] * N[i][i]
            for j in range (len(res)):
                resVectorCurrent[i] += M[i][j] * resVectorPrev[j]
            # yGraph[i].append(resVectorCurrent[i])
        change = sum(abs(np.subtract(resVectorCurrent, resVectorPrev)))
        # changeGraph.append(change)
        resVectorPrev = np.copy(resVectorCurrent)
        iter -= 1
    
    #setup dla wykresów, działają tylko dla układu 4x4    
    '''
    xGraph = [x for x in range(max(iter,orgIter)+1)]
    #graphConv(np.array(xGraph), np.array(yGraph), np.array(exp))
    if(exp is not None):
        graphPrec(xGraph[1:], changeGraph)
    '''

    #zwrócenie wektora rozwiązań
    return resVectorCurrent

def readMatrix(fileName):
    with open(fileName, encoding="utf8") as f:
        ret = [line.split() for line in f]
    return [[float(y) for y in x] for x in ret]

def readEq(fileName):
    with open(fileName, encoding="utf8") as f:
        ret = [line.rstrip('\n') for line in f]
        ret = list(map(float, ret))
    return ret

def graphConv(x, y, exp):

    plt.plot(x, y[0], label = "x1", color = "blue", alpha = 0.5)
    plt.plot(x, y[1], label = "x2", color = "red", alpha = 0.5)
    plt.plot(x, y[2], label = "x3", color = "yellow", alpha = 0.5)
    plt.plot(x, y[3], label = "x4", color = "green", alpha = 0.5)

    plt.plot(x, [exp[0]]*len(x), '--', color = "blue", linewidth = 2)
    plt.plot(x, [exp[1]]*len(x), '--', color = "red", linewidth = 2)
    plt.plot(x, [exp[2]]*len(x), '--', color = "yellow", linewidth = 2)
    plt.plot(x, [exp[3]]*len(x), '--', color = "green", linewidth = 2)

    plt.xlabel('iteracje')
    plt.ylabel('wartość')
    plt.title('Zbieganie do oczekiwanej wartości')
    plt.legend(loc='upper right')
    plt.show()

def graphPrec(x, y):

    plt.plot(x, y, label = "Precyzja", color = "blue")
    plt.xlabel('iteracje')
    plt.ylabel('wartość')
    plt.title('Zbieganie precyzji do 0')
    plt.legend(loc='upper right')
    plt.show()