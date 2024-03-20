from drivers.axis import Axis
from drivers.head import Head
#from drivers.gui import GUI
from drivers.perovskiteLib import *

#Constants for Axis Inputs
X_STEP_PIN = 18
X_DIR_PIN = 23
X_EN_PIN = 24
X_LIMIT = 1200
X_MOTOR_VAR = 0.001

Y_STEP_PIN = 12
Y_DIR_PIN = 5
Y_EN_PIN = 6
Y_LIMIT = 4800
Y_MOTOR_VAR = 0.0005

Z_STEP_PIN = 16
Z_DIR_PIN = 20
Z_EN_PIN = 21
Z_LIMIT = 3400
Z_MOTOR_VAR = 0.0008

#Create tuple constants for XYZ coords for things

#Create instances of the objects
x = Axis(X_STEP_PIN,X_DIR_PIN,X_EN_PIN,X_LIMIT,X_MOTOR_VAR)
y = Axis(Y_STEP_PIN,Y_DIR_PIN,Y_EN_PIN,Y_LIMIT,Y_MOTOR_VAR)
z = Axis(Z_STEP_PIN,Z_DIR_PIN,Z_EN_PIN,Z_LIMIT,Z_MOTOR_VAR)
p = Head()

