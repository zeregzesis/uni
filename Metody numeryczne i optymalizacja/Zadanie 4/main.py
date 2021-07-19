from num4 import *

# trygonometryczna
# a = 'sin(x)'

# who knows
# a = '4 / (1 + x**2)'

# złożenie?
# a = 'sin(1 / (x**2 + 1))'

# złożenie?
# a = 'sin(1 / (x**2 + exp(2*x)))'

# x^k
# a = 'x**5'

# eksponent
# a = 'exp(-x)'

x = symbols('x')
polys = [
    1, 
    x - 1, 
    x**2 - 4  * x    + 2, 
    x**3 - 9  * x**2 + 18  * x    - 6, 
    x**4 - 16 * x**3 + 72  * x**2 - 96   * x    + 24, 
    x**5 - 25 * x**4 + 200 * x**3 - 600  * x**2 + 600   * x    - 120, 
    x**6 - 36 * x**5 + 450 * x**4 - 2400 * x**3 + 5400  * x**2 - 4320  * x    + 720, 
    x**7 - 49 * x**6 + 882 * x**5 - 7350 * x**4 + 29400 * x**3 - 52920 * x**2 + 35230 * x - 5040
    ]

glLabel = "Całkowanie Gaussa-Laguerre'a"
ncLabel = 'Całkowanie Newtona-Cotesa'

if __name__ == '__main__':

    choice = input("Newton-Cotes[1], Gauss-Laguerre[2] lub porównanie metod[3]: ")

    if choice == '1':
        func = input('Podaj funkcję: ')
        start = input('Podaj początek: ')
        end = input('Podaj koniec: ')
        prec = input('Podaj precyzję: ')
        result, a = calkaNewtonaCotesa(start, end, func, prec)
        print("Wynik: " + str(float(result)))

    elif choice == '2':
        func = input('Podaj funkcję bez funkcji wagowej: ')
        nodes = int(input("Podaj ilość węzłów[2;5]:"))

        if nodes < 2 and nodes > 5:
            print("Zła liczba węzłów!")
            exit(1)

        result, a, b = calkaGaussaLaguerrea(func, nodes, polys)

        print("Wynik: " + str(float(result)))
    
    elif choice == '3':
        func = input('Podaj funkcję bez funkcji wagowej: ')
        prec = input('Podaj precyzję do metody Newtona-Cotesa: ')
        precL = input('Podaj precyzję dla granicy do metody Newtona-Cotesa: ')
        step = input("Podaj rozmiar kroku dla granicy do metody Newtona-Cotesa: ")
        nodes = int(input("Podaj ilość węzłów[2;5] dla matody Gaussa-Laguerre'a: "))

        if nodes < 2 and nodes > 5:
            print("Zła liczba węzłów!")
            exit(1)

        resultNC, a = ncIfn(func, precL, prec, step)
        resultGL, a, b = calkaGaussaLaguerrea(func, nodes, polys)

        print("Wynik Newtona: " + str(float(resultNC)) + "\nWynik Gaussa: " + str(resultGL))

    else:
        print("Zły wybór!")
        exit(2)