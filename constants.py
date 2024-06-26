'''
Constants Information File

Authors: ECD 415
         Pierce Alvir - Project Lead (CoE)
         Nicholas Blanchard - Mechanical Lead (ME)
         Steven Santamorena - Software Lead (CoE)
         Matthew Scott - Integration and Test Lead (ME)
         Luis Wang - Electrical Lead (EE)

Usage: File to store all the constants used throughout the project

'''
from dataclasses import dataclass

# Define a dataclass to make passing GPIO pins for motors less ugly/error-prone
@dataclass
class MotorPins:
    step: int # GPIO pin number for step pin
    dir: int # GPIO pin number for direction pin
    en: int # GPIO pin number for enable pin
    home: int # GPIO pin number for home switch pin (active low by the way)

#Microstepping Constants
X_MICROSTEP = 1
Y_MICROSTEP = 4
Z_MICROSTEP = 1

#X Constants
X_STEP_PIN = 18
X_DIR_PIN = 23
X_EN_PIN = 24
X_HOME_PIN = 4
X_LIMIT = 1140 * X_MICROSTEP
X_STEP_DELAY = 0.002
X_MOTOR_PINS = MotorPins(X_STEP_PIN, X_DIR_PIN, X_EN_PIN, X_HOME_PIN)

# 100 steps moves 19 mm = 0.19 mm per step = 0.00019 meters per step
X_ACCEL_CONST = 2500
X_MAX_DELAY = 0.0035 # 0.0035 sec/step = 285.714 steps/sec = 0.0542857 meters/sec
X_MIN_DELAY = 0.0002 # 0.0001 sec/step = 10000.0 steps/sec = 1.9 meters/sec

#Y Constants
Y_STEP_PIN = 12
Y_DIR_PIN = 5
Y_EN_PIN = 6
Y_HOME_PIN = 2
Y_LIMIT = 4840 * Y_MICROSTEP
Y_STEP_DELAY = 0.0010
Y_MOTOR_PINS = MotorPins(Y_STEP_PIN, Y_DIR_PIN, Y_EN_PIN, Y_HOME_PIN)
Y_ACCEL_CONST = 3000
Y_MIN_DELAY = 0.00025 # ~4000 steps/sec
Y_MAX_DELAY = None

#Z Constants
Z_STEP_PIN = 16
Z_DIR_PIN = 20
Z_EN_PIN = 21
Z_HOME_PIN = 3
Z_LIMIT = 4000 * Z_MICROSTEP
Z_STEP_DELAY = 0.001
Z_MOTOR_PINS = MotorPins(Z_STEP_PIN, Z_DIR_PIN, Z_EN_PIN, Z_HOME_PIN)
Z_ACCEL_CONST = 500
Z_MIN_DELAY = 0.001
Z_MAX_DELAY = 0.0015

#Head Constants
HEAD_STEP_PIN = 13
HEAD_DIR_PIN = 19
HEAD_EN_PIN = 26
HEAD_HOME_PIN = None
HEAD_VACUUM_PIN = 25
HEAD_MICROSTEP_MODE = 4
HEAD_STEPS_PER_UL = 150/200
HEAD_STEP_DELAY = 0.008
HEAD_MAX_UL = 200
HEAD_LIMIT = 300 #455 #275
UL_CORRECTION_FACTOR = 0.9
UL_CORRECTION_OFFSET = 2
HEAD_MOTOR_PINS = MotorPins(HEAD_STEP_PIN, HEAD_DIR_PIN, HEAD_EN_PIN, HEAD_HOME_PIN)

#Carousel Constants
CAROUSEL_STEP_PIN = 17
CAROUSEL_DIR_PIN = 27
CAROUSEL_EN_PIN = 22
CAROUSEL_HOME_PIN = None
CAROUSEL_VIAL = 8
CAROUSEL_STEP_DELAY = 0.008
CAROUSEL_MOTOR_PINS = MotorPins(CAROUSEL_STEP_PIN, CAROUSEL_DIR_PIN, CAROUSEL_EN_PIN, CAROUSEL_HOME_PIN)
CAROUSEL_ACCEL_CONST = 6000
CAROUSEL_MIN_DELAY = 0.00015

#Vial Constants
VIAL_SOLUTION_A = 1
VIAL_SOLUTION_B = 2
VIAL_SOLUTION_C = 3
VIAL_SOLUTION_D = 4
VIAL_ANTISOLVENT = 5
VIAL_CLEANER = 6
VIAL_EMPTY_A = 7
VIAL_EMPTY_B = 8

#Hot Plate Constants
HOTPLATE_EN_PIN = 7

#Spin Coater Constants
SPINCOATER_EN_PIN = 8

#Coordinate Constants yxz (make sure to add X_MICROSTEP and Z_MICROSTEP if we ever add that)
SLIDE_HOLDER = (486*Y_MICROSTEP,969,2943)
#SLIDE_HOLDER = (491*Y_MICROSTEP,975,2897) old one
DISPOSE_BIN = (100*Y_MICROSTEP,900,2500)
PIP_TO_TIP = (1340*Y_MICROSTEP,139,3740)
PIP_TO_VIAL = (3140*Y_MICROSTEP,816,667)
PIP_TO_SPIN = (4400*Y_MICROSTEP,499,2049)
CUP_TO_SPIN = (3765*Y_MICROSTEP,459,1478)
CUP_TO_HOT = (4835*Y_MICROSTEP,431,776)
TEMP_SLIDE_BIN = (4845,939,469)

