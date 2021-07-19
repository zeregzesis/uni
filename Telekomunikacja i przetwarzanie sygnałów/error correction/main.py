from funcFile import *

if __name__=='__main__':
    
    # macierz dla wykrywania i korekcji jednego błędu

    H = [
        [1, 0, 0, 1, 1, 1, 0, 0,    1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 1, 0,    0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1,    0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 1,    0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 1, 1,    0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 1,    0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0, 0,    0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1, 0,    0, 0, 0, 0, 0, 0, 0, 1]
    ]

    choice = input("Kodowanie(1) czy dekodowanie(2): ")
    if(choice == '1'):
        msg = input("Wpisz wiadomość do zapisania(bez polskich znaków): ")
        coded = encodeBlock(msgToBitArray(msg), H)
        mode = input("Zapis do pliku(1) czy wypisanie na konsoli(2): ")
        if(mode == '1'):
            fileName = input("Nazwa pliku do zapisu: ")
            saveToFile(coded, fileName)
            print("Zrobione!")
        elif(mode == '2'):
            print(coded)
        else:
            print("Niepoprawna opcja")
    elif(choice == '2'):
        fileName = input("Podaj nazwę pliku do odczytu: ")
        coded = readFromFile(fileName)
        decoded = decodeBlock(coded, H)
        msg = ""
        for row in decoded:
            msg += chr(bitlistToInt(row))
        print(msg)