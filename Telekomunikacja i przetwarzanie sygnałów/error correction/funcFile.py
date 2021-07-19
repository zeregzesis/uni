import numpy
from random import randint

# mnożenie macierzy
def matrixMult(m1, m2):
    result = numpy.matmul(m1,m2)
    result = numpy.mod(result, 2)
    return result.tolist()

# int na tablicę bitów
def bitfield(n):
    bitfield =  [int(digit) for digit in bin(n)[2:]]
    while (len(bitfield) != 8):
        bitfield.insert(0,0)
    return bitfield

# tablica bitów na int
def bitlistToInt(list_):
    return int("".join(str(x) for x in list_), 2)

# kodowanie wiadomości
def encode(msg, bitMatrix):
    parity = msg[:]
    for i in range(8):
        bit = 0
        for j in range(len(msg)):
            bit += msg[j] * bitMatrix[i][j]
        bit %= 2
        parity.append(bit)
    return (parity)

# dekodowanie wiadomości wraz z korekcją błędów
def decode(H, msg):

    # matrixMult to funkcja mnożenia macierzy wykożystująca numpy.matmul
    result = numpy.array(matrixMult(H, msg))
    control = result.sum()

    # sprawdzenie, czy wiadomość jest bezbłędna
    if(control == 0):
        # print("No errors detected")
        return msg[0:8]
    
    # jeśli wiadomość ma błędy:
    else:
        matrix = numpy.array(H)

        # sprawdzanie, czy istnieje jeden błąd i jego ewnetualne poprawienie
        for i in range(16):
            if(numpy.array_equal(result, matrix[:,i])):
                # print("Error at bit " + str(16 - i) + ". Result will be corrected")
                msg[i] = 1 - msg[i]
                return msg[0:8]

        # jeśli nie znaleziono jednego błędu, sprawdzanie gdzie są 2 błędy i ich poprawa
        for i in range(15):
            for j in range(i+1,16):
                columnSum = [(x + y)%2 for x, y in zip(matrix[:,i], matrix[:,j])]
                resultList = result.tolist()
                if(resultList == columnSum):
                    # print("Error at bits " + str(16 - i) + " and " + str(16-j) + ". Result will be corrected")
                    msg[i] = 1 - msg[i]
                    msg[j] = 1 - msg[j]
                    return msg[0:8]

# odczyt z pliku
def readFromFile(fileName):
    dividedMsg = []
    row = []
    counter = 0
    file = open(fileName, 'r')
    data = file.read()
    for bit in data:
        row.append(int(bit))
        counter += 1
        if(counter == 16):
            dividedMsg.append(row)
            row = []
            counter = 0
    return dividedMsg

# zapis do pliku
def saveToFile(msg, fileName):
    file = open(fileName, 'w')
    for bit in msg:
        file.write(str(bit))

# odkodowanie całej wiadomości(więcej niż 1 bajt)
def decodeBlock(block, H):
    resultArray = []
    for row in block:
        resultArray.append(decode(H, row))
    return resultArray

# kodowanie całej wiadomości(więcej niż 1 bajt)
def encodeBlock(block, bitMatrix):
    resultArray = []
    for row in block:
        resultArray += encode(row, bitMatrix)
    return resultArray

# string na tablicę bitów
def msgToBitArray(msg):
    resultArray = []
    for char in msg:
        resultArray.append(bitfield(ord(char)))
    return resultArray