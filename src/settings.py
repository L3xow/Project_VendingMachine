"""
PU = PushUp
JJ = JumpingJacks
SQ = Squats
LG = Lunges

RPi = Raspberry Pi

Reps = Wiederholungen.
"""

# Global Variables for managing the counters for the filling levels
actValueOne = 0
actValueTwo = 0
actValueThree = 0
actValueFour = 0
warningFour = 0
errorFour = 0

isClicked = False
counter = 0

# Settings to change the units
Tolerance = 0.8  # 80%

PUTime = 60             # seconds 60
PUReps = 20 * Tolerance  # 20

JJTime = 60  # 60
JJReps = 30 * Tolerance  # 30

SQTime = 60  # 60
SQReps = 30 * Tolerance  # 30

LGTime = 10  # 30
LGReps = 5 * Tolerance  # 20

CounterReset = 15

CamID = 1

#RPiIP = "192.168.2.41" # Tobi HomePi
#RPiIP = "192.168.137.61" # Tobi LaptopPi
RPiIP = "192.168.1.103" # Tobi NurembergPi

