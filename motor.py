# This Python file uses the following encoding: utf-8

from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep


factory = PiGPIOFactory(host='192.168.4.1') #IP of RASPI

'''
Motor1 = PIN 21
ES = Motor1 - 10 = PIN 11
Motor2 = PIN 22
ES = Motor2 - 10 = PIN 12

'''

def start(MotorID):

    if MotorID == 1:
        motor = 21
        es = 11
    elif MotorID == 2:
        motor = 22
        es = 12
    elif MotorID == 3:
        motor = 23
        es = 13
    elif MotorID == 4:
        motor = 24
        es = 14

    motorgo = LED(motor, pin_factory=factory)
    motorgo.on()
#    switch = Button(es, False)

#    if switch.wait_for_press():
#        sleep(2)
#        motorgo.off()




# if __name__ == "__main__":
#     pass
