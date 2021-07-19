from huffman_common import *

def socketClient(fileName, ip='127.0.0.1', port=42069):

    HOST = ip
    PORT = port

    file = open(fileName, 'rb')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(file.read())


def countChars(fileName): 

    file = open(fileName)

    handle = file.read()

    chars = [[],[]]

    for term in handle:

        if not term in chars[0]:
            chars[0].append(term)
            chars[1].append(1)

        else:
            chars[1][chars[0].index(term)] += 1

    numArr = np.array(chars, dtype="O")
    arr = numArr[:,numArr[1,:].argsort()]

    return arr[0], arr[1]


def nodesToDict(node, dictionary, val=''):

    newVal = val + str(node.huff)

    if(node.left):
        nodesToDict(node.left, dictionary, newVal)

    if(node.right):
        nodesToDict(node.right, dictionary, newVal)
 
    if(not node.left and not node.right):
        dictionary[newVal] = node.char


def encode(dictionary, messageFile):

    encodingDict = {v: k for k, v in dictionary.items()}

    bits = ""

    message = open(messageFile).read()

    for char in message:
        bits += encodingDict.get(char)
    
    # bits = bits[559:]
    bits = bs.BitArray(bin=bits)

    print(len(bits))

    with open("encoded.bnr", "wb") as f:
        while not len(bits) % 8 == 0:
            bits.bin += '0'
        f.write(bits.bytes)



def sendDict(fileToSave, dictionary, ip='127.0.0.1', port=42069):
  
    toSend = pickle.dumps(dictionary)
    file = open(fileToSave, 'wb')
    file.write(toSend)
    file.close()

    socketClient(fileToSave)


def sendMessage(fileName, ip='127.0.0.1', port=42069):

    socketClient(fileName, ip, port)


def createDict(fileName):
    
    chars, charCount = countChars(fileName)
    nodes = []
    
    for x in range(len(chars)):
        nodes.append(node(charCount[x], chars[x]))
    
    while len(nodes) > 1:

        nodes = sorted(nodes, key=lambda x: x.charCount)
    
        left = nodes[0]
        right = nodes[1]
    
        left.huff = 0
        right.huff = 1
    
        newNode = node(left.charCount+right.charCount, left.char+right.char, left, right)
    
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
    
    dictionary = {}
    nodesToDict(nodes[0], dictionary)

    return dictionary


if __name__ == "__main__":

    fileName = input("Nazawa pliku z danymi do wyslania: ")

    print("Plik podany")

    dictionary = createDict(fileName)
    
    print("Słownik stworzony")

    encode(dictionary, fileName)

    print("Zakodowane")

    sendDict('dict.txt', dictionary)

    print("Słownik wysłany")

    sendMessage("encoded.bnr")

    print("Wiadomość wysłana")