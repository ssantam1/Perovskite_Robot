from drivers.axis import Axis
from drivers.head import Head
#from drivers.gui import GUI
from drivers.perovskiteLib import *
import time

#Create tuple constants for XYZ coords for things
#PICK_UP_COORDS = (x,y,z)
#Create instances of the objects
x = Axis(X_STEP_PIN,X_DIR_PIN,X_EN_PIN,X_LIMIT,X_MOTOR_VAR)
y = Axis(Y_STEP_PIN,Y_DIR_PIN,Y_EN_PIN,Y_LIMIT,Y_MOTOR_VAR)
z = Axis(Z_STEP_PIN,Z_DIR_PIN,Z_EN_PIN,Z_LIMIT,Z_MOTOR_VAR)
p = Head()

def main():
    while True:
        print("Type 'demo()' to run pipette & z-axis demo")
	cmd = input(">> ")
	try:
	    exec(cmd)
	except Exception as E:
	    print(f"Error {E}, try again.")


# Executes whatever commands the user inputs
if __name__ == "__main__":
    main()

'''
help for time stuff
start = time.perf_counter()
end = time.perf_counter()
'''
