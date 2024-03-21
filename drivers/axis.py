'''

Axis Classes File

Created by Pierce Alvir and Steven Santamorena

Usage: Axis Movement Helper Classes

'''
import time
import board
import RPi.GPIO as GPIO
import constants

class XAxis(Stepper):
    def __init__(self, limit: int = None, step_delay1: int = None, step_delay2: int = None, microstep_mode: int = 1) -> None:
        step_pin = X_STEP_PIN
        dir_pin = X_DIR_PIN
        en_pin = X_EN_PIN
        limit = limit if limit else X_LIMIT
        step_delay1 = step_delay1 if step_delay1 else X_STEP_DELAY1
        step_delay2 = step_delay2 if step_delay2 else X_STEP_DELAY2
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay1, step_delay2, microstep_mode)

    def right(self, steps: int):
        self.positive(steps)

    def left(self, steps: int):
        self.negative(steps)

class YAxis(Stepper):
     def __init__(self, limit: int = None, step_delay1: int = None, step_delay2: int = None, microstep_mode: int = 1) -> None:
        step_pin = Y_STEP_PIN
        dir_pin = Y_DIR_PIN
        en_pin = Y_EN_PIN
        limit = limit if limit else Y_LIMIT
        step_delay1 = step_delay1 if step_delay1 else Y_STEP_DELAY1
        step_delay2 = step_delay2 if step_delay2 else Y_STEP_DELAY2
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay1, step_delay2, microstep_mode)


    def inward(self, steps: int):
        self.positive(steps)

    def outward(self, steps: int):
        self.negative(steps)
        
class ZAxis(Stepper):
     def __init__(self, limit: int = None, step_delay1: int = None, step_delay2: int = None, microstep_mode: int = 1) -> None:
         step_pin = Z_STEP_PIN
        dir_pin = Z_DIR_PIN
        en_pin = Z_EN_PIN
        limit = limit if limit else Z_LIMIT
        step_delay1 = step_delay1 if step_delay1 else Z_STEP_DELAY1
        step_delay2 = step_delay2 if step_delay2 else Z_STEP_DELAY2
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay1, step_delay2, microstep_mode)

    def up(self, steps: int):
        self.positive(steps)

    def down(self, steps: int):
        self.negative(steps)
