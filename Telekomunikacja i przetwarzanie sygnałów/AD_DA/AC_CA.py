import numpy as np
from scipy.io.wavfile import write, read
import soundcard as sc

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return abs(20*np.log10(abs(np.where(sd == 0, 0, m/sd))))

def record(timeInSecodns, sampleRate):
    microphone = sc.default_microphone()
    input("Naciśnij dowolny przycisk, aby rozpocząć nagrywanie")
    recorded = microphone.record(int(timeInSecodns * sampleRate), sampleRate, [0,1])
    print("Nagranie zakończone")
    return recorded

def saveToWav(dataToWrite, fileName, quantizationLevel, sampleRate):
    afterQuant = eval("np.int" + str(quantizationLevel) + "(dataToWrite/np.max(abs(dataToWrite)) * np.iinfo(\"int" + str(quantizationLevel) + "\").max)")
    write("{}.wav".format(fileName), sampleRate, afterQuant)

def playFromWav(fileName):
    speakers = sc.default_speaker()
    rawData = read(fileName)
    sampleRate = rawData[0]
    data = np.float64(rawData[1]/np.max(abs(rawData[1])))
    channels = [i for i in range(len(data[0]))]
    speakers.play(data, sampleRate, channels)
    print("SNR dla kolejnych kanałów:")
    snr = signaltonoise(data)
    for i in snr:   print("{}dB".format(str(round(i, 2))))

if __name__ == '__main__':

    choice = int(input("Nagrywanie[1] czy odtwarzanie[2]: "))

    if choice == 1:

        seconds = int(input("Podaj czas trwania nagrania w sekundach: "))

        sampleRate = int(input("Podaj częstotliwość próbkowania(-1 dla domyślnej wartości): "))
        if sampleRate < 0: sampleRate = 48000

        fileName = input("Podaj nazwę pliku(bez rozszerzenia) do zapisu nagrania: ")

        quantizationLevel = int(input("Podaj poziom kwantyzacji do zapisu(-1 dla domyślej wartości): "))
        if quantizationLevel < 0: quantizationLevel = 16

        saveToWav(record(seconds, sampleRate), fileName, quantizationLevel, sampleRate)

    elif choice == 2:

        fileName = input("Podaj ścieżkę do pliku(z rozszerzeniem) do odczytu: ")

        playFromWav(fileName)

    else:
        print("Zły wybór!")
        exit(1)