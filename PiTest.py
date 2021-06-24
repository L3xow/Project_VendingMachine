from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep


factory = PiGPIOFactory(host='192.168.4.1') #IP of RASPI


motor = 21

motorgo = LED(motor, pin_factory=factory)
motorgo.on()