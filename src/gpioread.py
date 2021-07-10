# This Python file uses the following encoding: utf-8

import pigpio


def readInput(input):
    """
    Funktion zum abfragen von RPi GPIO Status. Hier muss die IP des RPis geändert werden.

    :param input: (int) : Nummer des GPIO.
    :return: (bool) : True oder False je nach Schaltzustand des Eingangs.
    """
    pi = pigpio.pi("192.168.43.18", 8888)
    pi.set_mode(input, pigpio.INPUT)
    return pi.read(input)
