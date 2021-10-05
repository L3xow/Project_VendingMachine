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

PUTime = 20             # seconds 60
PUReps = 4 * Tolerance  # 20

JJTime = 10  # 60
JJReps = 2 * Tolerance  # 30

SQTime = 10  # 60
SQReps = 2 * Tolerance  # 30

LGTime = 20  # 30
LGReps = 4 * Tolerance  # 20

CounterReset = 15

CamID = 1

#RPiIP = "192.168.2.41" # Tobi HomePi
#RPiIP = "192.168.137.61 # Tobi LaptopPi
RPiIP = "192.168.1.103" # Tobi NurembergPi

