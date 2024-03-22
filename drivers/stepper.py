'''

Stepper Class File

Created by Pierce Alvir and Steven Santamorena

Usage: Inheritable class for other classes that utilize stepper motors

'''
import time
import board
import RPi.GPIO as GPIO

class Stepper():
    def __init__(self, step_pin: int, dir_pin: int, en_pin: int, limit: int, step_delay: int, flip_dir: bool = False, microstep_mode = 1) -> None:
        '''
        step_pin: int, GPIO pin number for step pin
        dir_pin: int, GPIO pin number for direction pin
        en_pin: int, GPIO pin number for enable pin
        limit: int, maximum number of steps the axis can move from zeroed position
        step_delay: int, delay between steps in seconds, controls speed of motor
        microstep_mode: int, number of microsteps per step, default is 1
        '''
        # Pin assignments
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin

        # Stepper settings
        self.steps_per_rev = 200 * microstep_mode #200 default with 1x microstepping
        self.limit = limit
        self.step_delay = step_delay
        self.flip_dir = flip_dir
        
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
            time.sleep(0.0001)

            GPIO.output(self.step_pin, 0)
            time.sleep(self.step_delay)

    def positive(self, steps: int):
        GPIO.output(self.dir_pin, 1 ^ self.flip_dir)
        self.move_steps(steps)
        self.pos += steps

    def negative(self, steps: int):
        GPIO.output(self.dir_pin, 0 ^ self.flip_dir)
        self.move_steps(steps)
        self.pos -= steps

if __name__ == "__main__":
    # Get motor parameters from user
    step_pin = int(input("Step Pin: "))
    dir_pin = int(input("Direction Pin: "))
    en_pin = int(input("Enable Pin: "))
    limit = int(input("Limit: "))
    step_delay = float(input("Step Delay: "))
    microstep_mode = int(input("Microstep Mode: "))
    stepper = Stepper(step_pin, dir_pin, en_pin, limit, step_delay, microstep_mode)

    while(True):
        print(f"Current Position: {stepper.pos}")
        cmd = "stepper."+input(">> ")
        try:
            exec(cmd)
        except Exception as E:
            print(f"Error {E}, try again.")
