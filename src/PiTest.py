from threading import Thread
import os, sys
from time import sleep


def funct1():
    count = 0
    while True:
        sleep(0.5)
        count += 1
        print(count, 0.5)


def funct2():
    count = 0
    while True:
        sleep(1)
        count += 1
        print(count, 1)


def main():
    Thread(target = funct1).start()
    Thread(target = funct2).start()

if __name__ == "__main__":
    main()