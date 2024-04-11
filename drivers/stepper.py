'''

Stepper Class File

Created by Pierce Alvir and Steven Santamorena

Usage: Inheritable class for other classes that utilize stepper motors

'''
import time
import board
import RPi.GPIO as GPIO
import numpy as np

class Stepper():
    def __init__(self, step_pin, dir_pin, en_pin, limit, step_delay, flip_dir = False, microstep_mode = 1) -> None:
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

    # Acceleration functions

    def gen_linear_decel(self, accel_const: int, min_delay: float, max_delay: float = 1) -> list[float]:
        delay_array = []
        delay = min_delay

        # When delay is negative, speed is negative so we need to stop cause we've collided with 0
        while delay >= 0 and delay <= max_delay:
            delay_array.append(delay)
            delay = 1 / ((-1 * delay * accel_const) + (1 / delay))

        return delay_array[:-1]

    def gen_movement_seq(self, num_steps: int, accel_constant: int, max_speed: float, min_speed: float = 1) -> list[float]:
        if num_steps == 0:
            return []

        decel_sequence = self.gen_linear_decel(accel_constant, max_speed, min_speed)
        accel_sequence = decel_sequence[::-1]

        accel_sequence = accel_sequence[:num_steps]
        decel_sequence = decel_sequence[-num_steps:]

        sequence = [max_speed] * num_steps
        for i in range(len(accel_sequence)):
            sequence[i] = max(accel_sequence[i], sequence[i])
        for i in range(len(decel_sequence)):
            sequence[-i-1] = max(decel_sequence[-i-1], sequence[-i-1])

        if max_speed in sequence:
            print("Profile type - Trapezoidal, max speed reached in sequence")
        else:
            print("Profile type - Triangular, max speed not reached in sequence")

        return sequence

    def move_smooth(self, num_steps: int, accel_constant: int, max_speed: float, min_speed: float = None):
        steps = self.gen_movement_seq(num_steps, accel_constant, max_speed, min_speed)

        for step in steps:
            GPIO.output(self.step_pin, 1)
            time.sleep(step)
            GPIO.output(self.step_pin, 0)
            time.sleep(0.00001)

    def accel_positive(self, num_steps: int, accel_constant: int, max_speed: int, min_speed: int = None):
        GPIO.output(self.dir_pin, 1 ^ self.flip_dir)
        self.move_smooth(num_steps, accel_constant, max_speed, min_speed)
        self.pos += num_steps

    def accel_negative(self, num_steps: int, accel_constant: int, max_speed: int, min_speed: int = None):
        GPIO.output(self.dir_pin, 0 ^ self.flip_dir)
        self.move_smooth(num_steps, accel_constant, max_speed, min_speed)
        self.pos -= num_steps

    def move_steps(self, steps: int):
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
    home_pin = int(input("Home Pin: "))
    limit = int(input("Limit: "))
    step_delay = float(input("Step Delay: "))
    flip_dir = bool(input("Flip Direction: "))
    microstep_mode = int(input("Microstep Mode: "))
    stepper = Stepper(step_pin, dir_pin, en_pin, home_pin, limit, step_delay, flip_dir, microstep_mode)

    while(True):
        print(f"Current Position: {stepper.pos}")
        cmd = "stepper."+input(">> ")
        try:
            exec(cmd)
        except Exception as E:
            print(f"Error {E}, try again.")
