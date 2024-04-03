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

    def move_smooth(self, num_steps: int, accel_constant: int, max_speed: float) -> np.ndarray:
        if num_steps == 0:
            return np.array([])
        
        def find_initial_speed(accel_constant: int, max_speed: float) -> float:
            speed = max_speed
            while True:
                new_speed = 1 / ((-1 * speed * accel_constant) + (1 / speed))
                if new_speed < 0:
                    return speed
                speed = new_speed

        def generate_acceleration_sequence(num_steps: int, acceleration_constant: int, max_speed: float) -> np.ndarray:
            steps = np.zeros(num_steps)
            steps[0] = find_initial_speed(acceleration_constant, max_speed)
            for i in range(1, num_steps):
                prev = steps[i-1]
                new_step = 1/((prev*acceleration_constant)+(1/prev))
                steps[i] = new_step
            steps = np.maximum(steps, max_speed)
            return steps

        accel_sequence = generate_acceleration_sequence(int(num_steps/2), accel_constant, max_speed)
        
        if num_steps % 2 == 0:
            decel_sequence = np.flip(accel_sequence)
        else:
            decel_sequence = np.flip(accel_sequence[:-1])
        
        steps = np.concatenate((accel_sequence, decel_sequence))

        for step in steps:
            GPIO.output(self.step_pin, 1)
            time.sleep(0.0001)

            GPIO.output(self.step_pin, 0)
            time.sleep(step)

    def accel_positive(self, num_steps: int, accel_constant: int, max_speed: int):
        GPIO.output(self.dir_pin, 1 ^ self.flip_dir)
        self.move_with_accel(num_steps, accel_constant, max_speed)
        self.pos += num_steps

    def accel_negative(self, num_steps: int, accel_constant: int, max_speed: int):
        GPIO.output(self.dir_pin, 0 ^ self.flip_dir)
        self.move_with_accel(num_steps, accel_constant, max_speed)
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
