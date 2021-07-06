# This Python file uses the following encoding: utf-8

import pigpio

def readInput(input):
    pi = pigpio.pi("192.168.137.231", 8888)
    pi.set_mode(input, pigpio.INPUT)
    return pi.read(input)
