from huffman_common import *

def socketServer(ip='127.0.0.1', port=42069):

    HOST = ip
    PORT = port

    file = open("output.txt", 'wb')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)

def decode(messageFile, dictionary):

    file = open("decoded.txt", 'w')
    message = ConstBitStream(filename='output.txt')

    # print(message)

    word = ""

    for i in range(len(message)):
        word += message.peek('bin:1')
        message.pos += 1

        if(dictionary.get(word, None)):
            file.write(dictionary.get(word))
            word = ""

def getDict(ip='127.0.0.1', port=42069):

    socketServer()
    serialized = open("output.txt", 'rb').read()
    dictionary = pickle.loads(serialized)
    return dictionary

def getMessage(ip='127.0.0.1', port=42069):

    socketServer()


if __name__ == "__main__":


    dictionary = getDict()

    print("Otrzymano słownik")

    getMessage()

    print("Otrzymano wiadomość")

    decode("output.txt", dictionary)

    print("Done!")
    '''
    import struct
    import bitstring as bs
    bits = "10111111111111111011110"  # example string. It's always 23 bits
    bits = "10111111111111111011110100111001"
    bits = bs.BitArray(bin=bits)


    print(type(bits))
    with open("test.bnr", "wb") as f:
        f.write(bits.bytes)
        #f.write(struct.pack('i', int(bits[::-1], 2)))

    from bitstring import ConstBitStream

    b = bs.ConstBitStream(filename='test.bnr')
    # print(b.read('bin:1'))

    print(b.peek('bin:1'))
    b.pos += 1
    print(b.peek('bin:1'))
    '''