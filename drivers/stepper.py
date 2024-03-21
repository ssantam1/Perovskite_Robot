'''

Stepper Class File

Created by Pierce Alvir and Steven Santamorena

Usage: Inheritable class for other classes that utilize stepper motors

'''
import time
import board
import RPi.GPIO as GPIO

class stepper():
    def __init__(self, step_pin: int, dir_pin: int, en_pin: int, limit: int, step_delay1: int, step_delay2: int, microstep_mode = 1) -> None:
        '''
        step_pin: int, GPIO pin number for step pin
        dir_pin: int, GPIO pin number for direction pin
        en_pin: int, GPIO pin number for enable pin
        limit: int, maximum number of steps the axis can move from zeroed position
        step_delay1: int, delay between steps in seconds, controls speed of motor
        step_delay2: int, delay between steps in seconds, controls speed of motor
        microstep_mode: int, number of microsteps per step, default is 1
        '''
        # Pin assignments
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin

        # Stepper settings
        self.steps_per_rev = 200 * microstep_mode #200 default with 1x microstepping
        self.limit = limit
        self.step_delay1 = step_delay1
        self.step_delay2 = step_delay2
        
        # Setup GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.output(self.en_pin,0)

        # Initialize position
        self.pos = 0

    def move_steps(self, steps: int):
        print(f"Moving {steps} steps")
        for _ in range(steps):
            GPIO.output(self.step_pin, 1)
            time.sleep(self.step_delay1)

            GPIO.output(self.step_pin, 0)
            time.sleep(self.step_delay2)

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
