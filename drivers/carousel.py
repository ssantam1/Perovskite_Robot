'''
Steven Santamorena 10/19/2023

This module is a rework of the carousel test script from the previous year, below is a list of some changes made:
- Turned carousel into a class to allow easier implementation as a module by other scripts
- Added move_steps() to reduce reduncancy
- Added step_sleep_time to make changes to step timing easier and less error-prone
- Removed unneeded imports and and motorkit setups that were never used
- Added type annotations for readability
- Added protection for out-of-bounds user inputs
- Added docstrings for all function defs
- Eliminated script code hidden in-between function defs that slowed down execution

To Do:
- Make inputs async
- Turn time.sleeps into async.sleeps
- Assess speed limitations
'''
import time
import asyncio
import board
import RPi.GPIO as GPIO
from drivers.stepper import Stepper
from constants import *

class Carousel(Stepper):
    '''Class that represents the carousel inside the Perovskite Synthesis System'''
    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        '''Initializes the carousel stepper motor'''
        limit = limit if limit else 99999 # arbitrary limit that is never reached
        step_delay = step_delay if step_delay else CAROUSEL_STEP_DELAY
        super().__init__(CAROUSEL_STEP_PIN, CAROUSEL_DIR_PIN, CAROUSEL_EN_PIN, CAROUSEL_HOME_PIN, limit, step_delay, microstep_mode)

        self.steps_per_rev = 200 # Number of steps per revolution on stepper motor
        self.num_vials = 8 # Number of vials/slots in the carousel
        self.current_vial = 1 # Current vial the carousel is at

    def reset_vial(self):
        '''Tell the carousel that it is at vial 1'''
        # This is mainly so I can do tests withou turning everything off and on again
        self.current_vial = 1

    # Define a method to move the carousel to a given vial
    def move_to_vial(self, target_vial: int) -> None:
        '''Moves the carousel to a desired vial and, sleeps for 3 seconds, and returns to original position'''
        # Check if the target vial is within the bounds of the carousel
        if target_vial < 1 or target_vial > self.num_vials:
            raise Exception("Vial numbers must be non-negative and not exceed num_vials-1")

        # Calculate the number of steps needed to move to the desired vial    
        steps_to_move = int(abs(target_vial - self.current_vial) * (self.steps_per_rev / self.num_vials))
 
        # Set the direction of the motor based on the target vial
        if target_vial > self.current_vial:
            GPIO.output(self.dir_pin,1)
        else:
            GPIO.output(self.dir_pin,0)

        # Move the motor to the target vial
        self.move_steps(steps_to_move)
        self.current_vial = target_vial

if __name__ == "__main__":
    c = Carousel()
    while(True):
        c.move_to_vial(int(input("Enter a vial number: ")))
