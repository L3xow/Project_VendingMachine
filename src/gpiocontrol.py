# This Python file uses the following encoding: utf-8

import pigpio

pi = pigpio.pi("192.168.137.61", 8888)
def readInput(input):
    """
    Funktion zum abfragen von RPi GPIO Status. Hier muss die IP des RPis geändert werden.

    :param input: (int) : Nummer des GPIO.
    :return: (bool) : True oder False je nach Schaltzustand des Eingangs.
    """
    pi.set_mode(input, pigpio.INPUT)
    val = pi.read(input)
    print("status " + str(val))
    return val

def writeOutput(output, level):
    """
    Funktion zum schalten von Ausgängen des RaspberryPis über Remote GPIo.

    :param output: (int) : GPIO des zu steuernden Ausgangs
    :param level: (bool) : Zustand des zu steuerenden Ausgangs: 0 = HIGH, 1 = LOW
    :return:
    """
    pi.set_mode(output, pigpio.OUTPUT)
    pi.write(output, level)