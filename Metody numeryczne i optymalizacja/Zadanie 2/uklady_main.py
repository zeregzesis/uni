from uklady_func import *

# exp = [2, -3, 1.5, 0.5]

fileName = input("Podaj nazwe pliku do wczytania wspolczynnikow: ")
matrix = readMatrix(fileName)

fileNameEq = input("Podaj nazwe pliku do wczytania wynikow rownan: ")
eq = readEq(fileNameEq)

if not checkMatrix(matrix):
    matrix, eq = fixMatrix(np.array(matrix), np.array(eq))
    if matrix is None:
        print("Macierz nie spelnia wymogow i nie mozna jej poprawic")
        exit(1)
    print("\nPoprawiona macierz wspolczynnikow:\n")
    print(matrix)
    print("\nPoprawiona macierz wynikow:\n")
    print(eq)
    print("\n")

if(checkMatrix(matrix) and len(matrix) == len(matrix[0]) and len(eq) == len(matrix)):
    choice = input("Ilosc iteracji[1] czy zadana precyzja[2]: ")
    if(choice == '1'):
        it = input("Podaj liczbe iteracji: ")
        # resVector = findResults(matrix, eq, int(it), 0, exp)
        resVector = findResults(matrix, eq, int(it), 0)
    elif(choice == '2'):
        prec = input("Podaj precyzje: ")
        # resVector = findResults(matrix, eq, -1, float(prec), exp)
        resVector = findResults(matrix, eq, -1, float(prec))
    else:
        print("Niepoprawny wybor.")
        exit(2)
else:
    print("Macierz nie spelnia wymogow i/lub nie mozna jej poprawic")
    exit(1)

print("\nWynik: ")
print(resVector)