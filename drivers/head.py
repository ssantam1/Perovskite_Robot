'''

Robotic Head Class File

Created by Pierce Alvir and Steven Santamorena

Usage: Class to operate robotic head mounted on the gantry

'''
import time 
import board
import RPi.GPIO as GPIO
from drivers.stepper import Stepper
from constants import *

class Head(Stepper):
    '''Class that represents the pipette inside the Perovskite Synthesis System'''

    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        self.limit = limit if limit else HEAD_LIMIT
        self.step_delay = step_delay if step_delay else HEAD_STEP_DELAY
        self.microstep_mode = microstep_mode if microstep_mode else HEAD_MICROSTEP_MODE
        super().__init__(HEAD_STEP_PIN, HEAD_DIR_PIN, HEAD_EN_PIN, self.limit, self.step_delay, flip_dir=False, microstep_mode=self.microstep_mode)
        
        self.vacuum_pin = HEAD_VACUUM_PIN # GPIO pin for the vacuum pump
        self.max_uL = HEAD_MAX_UL # Maximum volume of the pipette in microliters
        self.current_steps = 0 # Track the current position of the pipette in microliters

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.vacuum_pin, GPIO.OUT)

    # General motor control functions

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

    # Volume-based pipette actuation functions
        
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
      
    def vac_off(self):
        '''Turns off the vacuum pump'''
        GPIO.output(self.vacuum_pin, 0)

if __name__ == "__main__":
    # Give user control of the pipette for testing
    p = Head()
    while(True):
        print()
        print("==========[Commands]==========")
        print("down(steps) -- Moves the pipette finger down ")
        print("up(steps) ---- Moves the pipette finger up")
        print("down_uL(uL) -- Moves the pipette finger down a number of microliters")
        print("up_uL(uL) ---- Moves the pipette finger up a number of microliters")
        print("empty() ------ Empties the pipette of any fluid")
        print("lower_cup() -- Lowers the suction cup")
        print("raise_cup() -- Raises the suction cup")
        print("enable() ----- Turns on the motor")
        print("disable() ---- Turns off the motor")
        print("ctrl+C ------- Closes program")
        cmd = "p."+input(">> ")
        try:
            exec(cmd)
        except Exception as E:
            print(f"Error {E}, try again.")
