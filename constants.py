'''
Constants Information File

Created by Pierce Alvir and Steven Santamorena

'''
#Microstepping Constants
X_MICROSTEP = 1
Y_MICROSTEP = 2
Z_MICROSTEP = 1

#X Constants
X_STEP_PIN = 18
X_DIR_PIN = 23
X_EN_PIN = 24
X_HOME_PIN = 4
X_LIMIT = 1200 * X_MICROSTEP
X_STEP_DELAY = 0.001

#Y Constants
Y_STEP_PIN = 12
Y_DIR_PIN = 5
Y_EN_PIN = 6
Y_HOME_PIN = 2
Y_LIMIT = 4800 * Y_MICROSTEP
Y_STEP_DELAY = 0.0015


#Z Constants
Z_STEP_PIN = 16
Z_DIR_PIN = 20
Z_EN_PIN = 21
Z_HOME_PIN = 3
Z_LIMIT = 4000 * Z_MICROSTEP
Z_STEP_DELAY = 0.001

#Head Constants
HEAD_STEP_PIN = 13
HEAD_DIR_PIN = 19
HEAD_EN_PIN = 26
HEAD_HOME_PIN = None
HEAD_VACUUM_PIN = 25
HEAD_MICROSTEP_MODE = 4
HEAD_STEPS_PER_UL = 150/200
HEAD_STEP_DELAY = 0.008
HEAD_STEP_SLEEP_TIME = 0.05
HEAD_MAX_UL = 200
HEAD_LIMIT = 455 #275
UL_CORRECTION_FACTOR = 0.9
UL_CORRECTION_OFFSET = 2

#Carousel Constants
CAROUSEL_STEP_PIN = 17
CAROUSEL_DIR_PIN = 27
CAROUSEL_EN_PIN = 22
CAROUSEL_HOME_PIN = None
CAROUSEL_VIAL = 8
CAROUSEL_STEP_DELAY = 0.006
CAROUSEL_STEP_SLEEP_TIME = 0.0001 #not sure if this gets used but it was in carousel file

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
SLIDE_HOLDER = (564*Y_MICROSTEP,951,3364)
DISPOSE_BIN = (100*Y_MICROSTEP,900,2500)
PIP_TO_TIP = (1295*Y_MICROSTEP,3,3765)
PIP_TO_VIAL = (3150*Y_MICROSTEP,450,664)
PIP_TO_SPIN = (4400*Y_MICROSTEP,522,1670)
SUC_TO_SPIN = (3859*Y_MICROSTEP,420,1424)
SUC_TO_HOT = None

