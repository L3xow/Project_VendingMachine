# This Python file uses the following encoding: utf-8

import gpiozero
import os

import pigpio
from time import sleep

#factory = PiGPIOFactory(host='192.168.137.231') #IP of RASPI

'''
Motor1 = PIN 21
ES = Motor1 - 10 = PIN 11
Motor2 = PIN 22
ES = Motor2 - 10 = PIN 12

'''

def start(MotorID):
    pi = pigpio.pi("192.168.137.231", 8888)
    while pi.connected:
        if MotorID == 1:
            motor = 21
            es = 20
        elif MotorID == 2:
            motor = 22
            es = 12
        elif MotorID == 3:
            motor = 23
            es = 13
        elif MotorID == 4:
            motor = 24
            es = 14

        pi.set_mode(motor, pigpio.OUTPUT)
        pi.set_mode(es, pigpio.INPUT)

        if not pi.read(es):
            pi.write(motor, 1)
            sleep(2)
            pi.write(motor, 0)
            break



#    button = Button(20)
#    button.wait_for_press()
#    print("The button was pressed!")

#    switch = Button(es, False)

#    if switch.wait_for_press():
#        sleep(2)
#        motorgo.off()

def main():
    start(1)

if __name__ == "__main__":
    main()