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

    steps_per_rev = 200 # Number of steps per revolution on stepper motor
    num_vials = 8 # Number of vials/slots in the carousel
    step_sleep_time = 0.0001 # Time to sleep in between turning on and off GPIO for steps

    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = CAROUSEL_STEP_PIN
        dir_pin = CAROUSEL_DIR_PIN
        en_pin = CAROUSEL_EN_PIN
        limit = limit if limit else 1200 #random limit that i am putting
        step_delay = step_delay if step_delay else CAROUSEL_STEP_DELAY
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay, microstep_mode)

    # Define a method to move the carousel to a given vial
    def move_to_vial(self, vial_position: int) -> None:
        '''Moves the carousel to a desired vial and, sleeps for 3 seconds, and returns to original position'''
        # Calculate the number of steps needed to move to the desired vial
        steps_to_move = int(((vial_position-1) / self.num_vials) * (self.steps_per_rev))

        # Move the stepper motor to the desired position
        print("swapping dir to 1")
        GPIO.output(self.dir_pin,1)
        self.move_steps(steps_to_move)

        # Pause for the specified delay before returning to the original position
        time.sleep(1)

        # Move the stepper motor back to the original position
        print("swapping dir to 0")
        GPIO.output(self.dir_pin,0)
        self.move_steps(steps_to_move)

    # Define a function to handle user input and move the carousel to the desired vials
    def move_to_vials(self):
        '''Takes input sequence from user and calls move_to_vial() for each item'''
        # Prompt the user for the desired vials
        vial_sequence: str = input('Enter the desired vials in order (e.g. 1,3,5): ')

        # Split the user input into individual vials
        vials: list[str] = vial_sequence.split(',')

        # Move the carousel to each desired vial in turn
        for vial in vials:
            vial = int(vial)

            # Raise exception if a vial number is too high or too low
            if vial < 0 or vial > self.num_vials:
                raise Exception("Vial numbers must be non-negative and not exceed num_vials-1")
            
            # Begin rotating carousel
            self.move_to_vial(vial)
            time.sleep(1)

if __name__ == "__main__":
    c = Carousel()
    while(True):
        c.move_to_vials()
