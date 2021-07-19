import serial
import time
import serial.tools.list_ports as lp

SOH = b'\x01'
EOT = b'\x04'
ACK = b'\x06'
NAK = b'\x15'
ETB = b'\x17'
CAN = b'\x18'
C   = b'\x43'

def config():

    ports = [port for port in sorted(lp.comports())]
    res_ports = []
    print("Dostępne porty: ")
    i = 0
    for port, desc, hwid in ports:
        res_ports.append(port)
        print(str(i) + ". " + port)
        i += 1
    if len(res_ports) == 0: exit("Brak dostępnych portów")
    choice = res_ports[int(input("Wybierz: "))]

    ser = serial.Serial(choice, timeout=3, inter_byte_timeout=1)
    ser.flush()
    return ser

def crcSum(data : bytes):

    data = bytearray(data)
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return (crc & 0xFFFF).to_bytes(2, "big")

def ctrlSum(data : bytes):

    # funkcja generująca sumę algebraiczną
    data = bytearray(data)
    result = 0
    for byte in data:
        result += byte
        result %= 256
    return result.to_bytes(1, "big")

def openCom(ser, crc):

    counter = 0
    while counter < 6:
        if not crc:
            ser.write(NAK)
            msg = ser.read(132)
        else:
            ser.write(C)
            msg = ser.read(133)
        
        if not msg == b'':
            return True, msg

        counter += 1
        time.sleep(10)
    
    return False, None


def reciever(ser, crc):

    # nazwa pliku do zapisu
    output = open(input("Nazwa pliku do zapisu: "), 'wb')

    # otwarcie połączenia
    status, msg = openCom(ser, crc)

    #jeśli otwarcie się nie powiodło, wyjdź z programu
    if not status == True:
        return False

    blocknum = 1

    while True:
        # sprawdzenie czy otrzymujemy właściwy nagłówek
        if not msg[0:1] == SOH:
            return False
        if not blocknum == msg[1]:
            return False
        if not 255 - blocknum == msg[2]:
            return False
        
        # wydzielenie sekcji z danymi
        dec = msg[3:131]

        # liczenie sumy kontrolnej
        if not crc:
            ctrl = ctrlSum(dec)
            ctrlT = msg[131:132] 
        else:
            ctrl = crcSum(dec)
            ctrlT = msg[131:133]
        
        # sprawdzenie zgodności sum kontrolnych i odpowiednia odpowiedź
        if ctrl == ctrlT:
            ser.write(ACK)
            output.write(dec)
            blocknum += 1
        else:
            ser.write(NAK)

        # odczyt następnego/ponowionego bloku danych
        if not crc:
            msg = ser.read(132)
        else:
            msg = ser.read(133)
        
        # jeśli osiągnięto koniec transmisji, odpowiedz i zakończ
        if msg == EOT:
            ser.write(ACK)
            break

def fileRead(file):
    flag = False
    content = file.read(128)
    while len(content) < 128:
        content += b'\x00'
        flag = True
    return content, flag

def sender(ser):

    # definicja i odczyt potrzebnych danych
    blockNum = 1
    sendFile = open(input("Nazwa pliku do przeslania: "), 'rb')
    initChar = ser.read()

    # nasłuch na porcie
    while initChar == b'':
        initChar = ser.read()

    flag = False

    while not flag:

        # odczyt 128 bajtów danych z pilku
        block, flag = fileRead(sendFile)

        # liczenie sumy kontrolnej
        if initChar == NAK:
            ctrl = ctrlSum(block)
        elif initChar == C:
            ctrl = crcSum(block)

        # formatowanie pakietu do wysłania
        block = SOH + blockNum.to_bytes(1, "big") + (255-blockNum).to_bytes(1, "big") + block + ctrl

        # wysłanie pakietu i reakcja na ew. prośbę ponowienia
        ser.write(block)
        char = ser.read()
        while char == NAK:
            ser.write(block)
            char = ser.read()

        blockNum += 1

    # wysłanie EOT, gdy cały plik jest przesłany
    ser.write(EOT)


if __name__ == "__main__":

    ser = config()
    choice = int(input("Wysylanie(1), czy odbieranie(2): "))

    if choice == 1:
        sender(ser)

    elif choice == 2:
        ctrl = int(input("Suma algebraiczna(1) czy CRC(2): "))
        reciever(ser, (ctrl == 2))

    else:
        print("Zly wybor")