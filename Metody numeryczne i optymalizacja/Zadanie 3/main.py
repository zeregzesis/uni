from lagrange import chebyshev, fromFile, calculateY, lagrange, graphCompare

if __name__ == "__main__":
    
    mode = input("Wezly Czebyszewa(1) czy podane punkty(2): ")
    if mode == '1':

        start = input("Poczatek przedzialu: ")
        end = input("Koniec przedzialu: ")
        nodes = input("Ilosc wezlow: ")
        xTab = chebyshev(float(start), float(end), int(nodes))
        print(xTab)

    elif mode == '2':

        fileName = input("Nazwa pliku do wczytania punktow: ")
        xTab = fromFile(fileName)

    else:

        print("Zly wybor!")
        exit(1)

    func = input("Funkcja: ")
    yTab = calculateY(xTab, func)

    newFunc = lagrange(xTab, yTab)

    print(newFunc)

    graphCompare(func, newFunc, xTab)