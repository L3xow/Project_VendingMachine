# This Python file uses the following encoding: utf-8

import pigpio
from time import sleep


'''
Motor1 = PIN 21
ES = Motor1 - 10 = PIN 11
Motor2 = PIN 22
ES = Motor2 - 10 = PIN 12

'''

def start(MotorID, time = 5.8):
    """
    Funktion zum ansteuern der Motoren. Es wird eine ID übergeben, (1-4) mit der die GPIO bereits vorkonfiguriert sind.
    Es wird zunächst eine IP Verbindung zum RPi aufgebaut, um dann die Status der GPIO abzufragen, bzw diese anzusteuern.
    Anschließend werden die GPIO Pins vorbereitet, in diesem Fall auf Input oder Output konfiguriert.
    GPIOs werden dann angesteuert oder, je nachdem ob es ein Eingang ist, abgefragt.

    :param MotorID: (int) : Wert zwischen 1-4, Motor nummerierung von Links nach Rechts.
    :return:
    """
    pi = pigpio.pi("192.168.137.61", 8888)
#    pi = pigpio.pi("192.168.2.41", 8888)
    while pi.connected:
        if MotorID == 1:
            motor = 21
            es = 22
        elif MotorID == 2:
            motor = 20
            es = 27
        elif MotorID == 3:
            motor = 16
            es = 17
        elif MotorID == 4:
            motor = 12
            es = 24

        pi.set_mode(motor, pigpio.OUTPUT)
        pi.set_mode(es, pigpio.INPUT)

        pi.write(motor, 0)
        sleep(time)
        pi.write(motor, 1)
        return True




def main():
    """
    Testfunktion wenn kein Aufruf von außerhalb.

    :return:
    """
    start(1)

if __name__ == "__main__":
    main()