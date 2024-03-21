'''

Axis Classes File

Created by Pierce Alvir and Steven Santamorena

Usage: Axis Movement Helper Classes

'''
import time
import board
import RPi.GPIO as GPIO
from constants import *
from drivers.stepper import Stepper

class XAxis(Stepper):
    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = X_STEP_PIN
        dir_pin = X_DIR_PIN
        en_pin = X_EN_PIN
        limit = limit if limit else X_LIMIT
        step_delay = step_delay if step_delay else X_STEP_DELAY
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay, microstep_mode)

    def positive(self, steps: int):
        GPIO.output(self.dir_pin, 1)
        self.move_steps(steps)
        self.pos += steps

    def negative(self, steps: int):
        GPIO.output(self.dir_pin, 0)
        self.move_steps(steps)
        self.pos -= steps

    def right(self, steps: int):
        self.positive(steps)

    def left(self, steps: int):
        self.negative(steps)

class YAxis(Stepper):
    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = Y_STEP_PIN
        dir_pin = Y_DIR_PIN
        en_pin = Y_EN_PIN
        limit = limit if limit else Y_LIMIT
        step_delay = step_delay if step_delay else Y_STEP_DELAY
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay, microstep_mode)

    def positive(self, steps: int):
        GPIO.output(self.dir_pin, 0)
        self.move_steps(steps)
        self.pos += steps

    def negative(self, steps: int):
        GPIO.output(self.dir_pin, 1)
        self.move_steps(steps)
        self.pos -= steps

    def inward(self, steps: int):
        self.positive(steps)

    def outward(self, steps: int):
        self.negative(steps)
        
class ZAxis(Stepper):
    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = Z_STEP_PIN
        dir_pin = Z_DIR_PIN
        en_pin = Z_EN_PIN
        limit = limit if limit else Z_LIMIT
        step_delay = step_delay if step_delay else Z_STEP_DELAY
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay, microstep_mode)

    def positive(self, steps: int):
        GPIO.output(self.dir_pin, 0)
        self.move_steps(steps)
        self.pos += steps

    def negative(self, steps: int):
        GPIO.output(self.dir_pin, 1)
        self.move_steps(steps)
        self.pos -= steps

    def up(self, steps: int):
        self.negative(steps)

    def down(self, steps: int):
        self.positive(steps)
