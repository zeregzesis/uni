import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi, tan


def turnToTable(eqString):

    table = [[],[]]
    counter = 0
    powSwitch = 0
    valSwitch = 0
    digit = ''
    pow = ''

    for char in eqString:

        if char == ' ':

            print(digit)

            if valSwitch == 1:
                digit = '-' + digit
                valSwitch = 0

            if powSwitch == 1:

                table[0][counter] = float(pow)
                powSwitch = 0
                pow = ''

                table[1].append(float(digit))
                digit = ''

                counter += 1
                continue

            if not digit == '' and not digit == '-':
                table[0].append(0)
                table[1].append(float(digit))
                digit = ''
                counter += 1
                continue

            continue

        if char == 'x':
            table[0].append(1)
            continue

        if char == '^':
            powSwitch = 1
            continue

        if char == '-':
            valSwitch = 1
            continue

        if char == '+':
            valSwitch = 0
            continue

        if powSwitch == 1:
            pow += char
            continue

        digit += char
        print(digit)
    
    if not digit == '':
        table[1].append(float(digit))

    return table


def bracketMult(t1, t2):
    """Funkcja mnożenia dwóch nawiasów z niewiadomą x

    Argumenty:
        t1 - pierwszy z nawiasów w formie tabeli
        t2 - drugi z nawiasów w formie tabeli

    Zwraca:
        Pomnożone nawiasy z niewiadomą w formie tabeli
    """

    temp = [[],[]]

    for i in range (len(t1[0])):
        for j in range(len(t2[0])):
            temp[0].append(t1[0][i] + t2[0][j])
            temp[1].append(t1[1][i] * t2[1][j])
        
    return tabAdd(temp)


def tabAdd(tab):
    """Dodanie wyrazów o tej samej potędze w tabeli reprezentującej równanie z niewiadomą x

    Argumenty:
        tab - tabela reprezentująca równanie z niewiadomą x

    Zwraca:
        Tabelę z dodanymi wyrazami o tej zamej potędze
    """

    m = max(tab[0])
    result = [[0 for x in range(m+1)],[0 for x in range(m+1)]]

    for i in range (len(tab[0])):
        result[0][abs(tab[0][i]-m)] = tab[0][i]       # do optymalizaji(przenieść potęgi do deklaracji i pozbyć się tej linii)
        result[1][abs(tab[0][i]-m)] += tab[1][i]

    return result


def tabToHorner(tab):
    """Konwersja tabeli reprezentującej równanie z niewiadomą x na równanie schematem Hornera

    Argumenty:
        tab - tabela reprezentująca równanie z niewiadomą x

    Zwraca
        Równanie schematem Hornera na bazie tabeli
    """

    result = ""

    for _ in range(tab[0][0]-1):
        result += "("

    result += str(tab[1][0]) + "*x" 

    if tab[1][1] > 0:
        result += "+"

    result += str(tab[1][1])

    for i in range(2, len(tab[1])):
        result += ")*x"

        if tab[1][i] >= 0:
            result += "+"
        
        result += str(tab[1][i])
    
    return result


def evalUserFunc(func, xTab):
    """Wyliczenie wartości zadanej funkcji dla podanych punktów

    Argumenty:
        func - funkcja, dla której liczone mają być wartości, w formie tekstu
        xTab - lista punktów dla których liczona jest wartość funkcji

    Zwraca:
        Listę wartości funkcji w zadanych punktach
    """

    res = []
    func.replace('^','**')

    for x in xTab:
        res.append(eval(func))
    
    return res


def lagrange(xTab, yTab):
    """Realizacja wielomianu interpolacyjnego Lagrange'a

    Argumenty:
        xTab - punkty na bazie których liczony będzie wielomian
        yTab - wartości w tych punktach dla oryginalnej funkcji

    Zwraca:
        Wielomian interpolacyjny w postaci Hornera
    """

    agr = []

    for i in range(len(yTab)):

        tab = []
        div = 1
        for j in range(len(yTab)):
            if not j == i:
                temp = [[1,0],[1,-xTab[j]]]
                tab.append(temp)
                div *= xTab[i]-xTab[j]

        temp = tab[0]

        for j in range(1, len(tab)):
            temp = bracketMult(temp, tab[j])

        for j in range(len(temp[1])):
            temp[1][j] /= div
            temp[1][j] *= yTab[i]
        
        agr.append(temp)

    temp = agr[0]
    for i in range(1, len(agr)):
        for j in range(2):
            temp[j] += agr[i][j]
    
    temp = tabAdd(temp)

    result = tabToHorner(temp)

    return result


def fromFile(fileName):

    with open(fileName, encoding="utf8") as f:
        ret = [line.split() for line in f]

    return [[float(y) for y in x] for x in ret][0]


def calculateY(xTab, eq):

    yTab = []

    for x in xTab:
        yTab.append(eval(eq))

    return yTab


def chebyshev(a, b, n):
    """Wyznaczanie węzłów Czebyszewa

    Argumenty:
        a - początek przedziału
        b - koniec przedziału
        n - liczba węzłów do wyznaczenia

    Zwraca:
        Listę wyznaczonych n węzłów Czebyszewa dla przedziału [a;b]
    """

    result = []

    for k in range(n):
        temp = cos( (pi/2) * (2*k+1)/(n) )
        temp = round(temp, 8)
        print(temp)
        result.append((a+b)/2 + temp*(b-a)/2)

    return result


def avgError(xTab, funcOrg, funcRes):

    errorTab = 0
    for x in xTab:
        errorTab += abs(eval(funcOrg) - eval(funcRes))

    return errorTab/len(xTab)


def errorAtPoint(x, funcOrg, funcRes):

    return abs(eval(funcOrg) - eval(funcRes))


def graphSingle(func):

    x = np.linspace(-10, 10, 100)
    y = eval(func)

    plt.plot(x, y)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Wykres funkcji ' + func)

    plt.show()


def graphCompare(funcOrg, funcRes, xOrg):
    """Rysowanie wykresu porównawczego funkcji oryginalnej i uzyskanego z interpolacji wielomianu

    Argumenty:
        funcOrg - tekstowa reprezentacja oryginalnej funkcji
        funcRes - tekstowa reporezentacja funkcji wielomianowej uzyskanej z interpolacji
        xOrg - oryginalne punkty, na których przeprowadzana była interpolacja

    Zwraca:
        Nic

    Wyświetla:
        Wykres zestawiający obydwie funkcje oraz oryginalne punkty
    """

    x = np.array(xOrg)
    yComp = eval(funcOrg)

    x = np.linspace(-10, 10, 10000)
    y1 = eval(funcOrg)
    y2 = eval(funcRes)

    plt.plot(x, y1, label = "Oryginalna funkcja", color = "blue")
    plt.plot(x, y2, label = "Funkcja uzyskana z interpolacji", color = "red")
    plt.plot(xOrg, yComp, 'gD', linestyle='None', label = "Oryginalne punkty")

    error = round(avgError(x, funcOrg, funcRes), 4)
    plt.plot([], [], ' ', label="Średni błąd interpolacji: " + str(error))

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Porównanie wykresów funkcji oryginalnej i uzyskanej z interpolacji')
    plt.legend()

    plt.show()

def generateRandomPoints(numberOfPoints):
    import random as r
    import numpy as np
    nums = []
    for _ in range(numberOfPoints):
        nums.append(round(r.uniform(-10,10), 2))
    nums.sort()
    return np.array(nums)