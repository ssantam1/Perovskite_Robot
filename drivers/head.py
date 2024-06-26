'''

Robotic Head Class File

Authors: ECD 415
         Pierce Alvir - Project Lead (CoE)
         Nicholas Blanchard - Mechanical Lead (ME)
         Steven Santamorena - Software Lead (CoE)
         Matthew Scott - Integration and Test Lead (ME)
         Luis Wang - Electrical Lead (EE)

Usage: Class to operate robotic head mounted on the gantry

'''
import time

import board
import RPi.GPIO as GPIO

from drivers.stepper import Stepper
from constants import *  # Should change to import as const for PEP 8.

class Head(Stepper):
    '''
    Class that represents the pipette/suction cup tool head
    '''
    def __init__(self,
        limit: int = None,
        step_delay: int = None,
        microstep_mode: int = 1) -> None:
        '''
        Initializes the head stepper motor
        
        Args:
            limit (int, optional): The maximum step limit for the axis.
            step_delay (int, optional): The delay between steps in seconds.
            microstep_mode (int, optional): The microstep factor. Default: 1
        '''
        self.limit = limit if limit else HEAD_LIMIT
        self.step_delay = step_delay if step_delay else HEAD_STEP_DELAY
        self.microstep_mode = microstep_mode if microstep_mode else HEAD_MICROSTEP_MODE
        super().__init__(HEAD_STEP_PIN,
            HEAD_DIR_PIN,
            HEAD_EN_PIN,
            self.limit,
            self.step_delay,
            flip_dir=False,
            microstep_mode=self.microstep_mode)
        
        self.vacuum_pin = HEAD_VACUUM_PIN  # GPIO pin for the vacuum pump.
        self.max_uL = HEAD_MAX_UL  # Max vol of the pipette in microliters.
        self.current_steps = 0  # The current position of the motor in steps.

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.vacuum_pin, GPIO.OUT)

    # General motor control functions:

    def down(self, steps: int):
        '''Moves the pipette plunger down a number of steps'''
        self.positive(steps)
        self.current_steps += steps
        print(f"current_steps = {self.current_steps}")
        
    def up(self, steps: int):
        '''Moves the pipette plunger up a number of steps'''
        self.negative(steps)
        self.current_steps -= steps
        print(f"current_steps = {self.current_steps}")

    # Volume-based pipette actuation functions:
        
    def volume_to_steps(self, uL: int) -> int:
        '''Corrects the volume of the pipette to account for linear error'''
        corrected_uL = ((uL * UL_CORRECTION_FACTOR) + UL_CORRECTION_OFFSET)
        return int(HEAD_STEPS_PER_UL * corrected_uL)
        
    def down_uL(self, uL: int):
        '''Moves the pipette plunger down a number of microliters'''
        steps = self.volume_to_steps(uL)
        print(f"Pipette moving {steps} steps ({uL} uL) down...")
        self.down(steps)
        
    def up_uL(self, uL: int):
        '''Moves the pipette plunger up a number of microliters'''
        steps = self.volume_to_steps(uL)
        print(f"Pipette moving {steps} steps ({uL} uL) up...")
        self.up(steps)

    def empty(self):
        '''Empties the pipette of any fluid'''
        steps_to_empty = int(self.max_uL * HEAD_STEPS_PER_UL) - self.current_steps
        print(f"Emptying pipette of {steps_to_empty} steps...")
        self.down(steps_to_empty)
        time.sleep(0.2)
        self.up(int(self.max_uL * HEAD_STEPS_PER_UL))
    
    # Suction cup functions

    def lower_cup(self):
        '''Lowers the suction cup to below pipette tip'''
        self.up(self.limit)

    def raise_cup(self):
        '''Raises the suction cup to above pipette tip'''
        self.down(self.limit)

    def vac_on(self):
        '''Turns on the vacuum pump'''
        GPIO.output(self.vacuum_pin, 1)
        time.sleep(1)
      
    def vac_off(self):
        '''Turns off the vacuum pump'''
        GPIO.output(self.vacuum_pin, 0)
        time.sleep(1)

if __name__ == "__main__":
    # Run with -i flag to test any functions of the head
    p = Head()
