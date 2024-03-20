'''

Created by Pierce Alvir and Steven Santamorena

'''
import time
import board
import RPi.GPIO as GPIO

'''
These are how to instantiate x, y, and z

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

x = Axis(X_STEP_PIN,X_DIR_PIN,X_EN_PIN,X_LIMIT,X_MOTOR_VAR)
y = Axis(Y_STEP_PIN,Y_DIR_PIN,Y_EN_PIN,Y_LIMIT,Y_MOTOR_VAR)
z = Axis(Z_STEP_PIN,Z_DIR_PIN,Z_EN_PIN,Z_LIMIT,Z_MOTOR_VAR)
'''

class Axis(step_pin: int, dir_pin: int, en_pin: int, limit: int, motor_var: float):
    def __init__(self):
        self.steps_per_rev = 200 # Number of steps per revolution on stepper motor
        self.step_sleep_time = 0.001 # Time to sleep in between turning on and off GPIO for steps
        
        self.pos = 0
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        self.limit = limit
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.output(self.en_pin,0)

    def move_steps(self, steps: int):
        print(f"Moving {steps} steps")
        for _ in range(steps):
            GPIO.output(self.step_pin, 1)
            time.sleep(0.0005)

            GPIO.output(self.step_pin, 0)
            time.sleep(motor_var)

    def positive(self, steps: int):
        GPIO.output(self.dir_pin, 1)
        self.move_steps(steps)
        self.pos += steps

    def negative(self, steps: int):
        GPIO.output(self.dir_pin, 0)
        self.move_steps(steps)
        self.pos -= steps

    
if __name__ == "__main__":
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
    x = Axis(X_STEP_PIN,X_DIR_PIN,X_EN_PIN,X_LIMIT,X_MOTOR_VAR)
    y = Axis(Y_STEP_PIN,Y_DIR_PIN,Y_EN_PIN,Y_LIMIT,Y_MOTOR_VAR)
    z = Axis(Z_STEP_PIN,Z_DIR_PIN,Z_EN_PIN,Z_LIMIT,Z_MOTOR_VAR)
    while(True):
        print(f"pos{x.pos}")
        cmd = "x."+input(">> ")
        try:
            exec(cmd)
        except Exception as E:
            print(f"Error {E}, try again.")
