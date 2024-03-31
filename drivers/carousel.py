import board
import RPi.GPIO as GPIO
from drivers.stepper import Stepper
from constants import *

class Carousel(Stepper):
    '''Class that represents the carousel inside the Perovskite Synthesis System'''
    def __init__(self, step_delay: int = CAROUSEL_STEP_DELAY, microstep_mode: int = 1) -> None:
        '''Initializes the carousel stepper motor'''
        super().__init__(CAROUSEL_STEP_PIN, CAROUSEL_DIR_PIN, CAROUSEL_EN_PIN, CAROUSEL_HOME_PIN, None, step_delay, microstep_mode=microstep_mode)

        self.steps_per_rev = 200 * microstep_mode # Number of steps per revolution on stepper motor
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
    # Run with -i flag to test any functions of the carousel
    c = Carousel()
    
    # Show a list of available functions for carousel/stepper
    print("Carousel initialized as 'c'")
    print("Available Carousel Functions:")
    print("c.move_to_vial(target_vial) ---> Moves the carousel to the target vial")
    print("c.reset_vial() ----------------> Defines the current vial as vial 1")
    print("c.move_steps(num_steps) -------> Moves the carousel a certain number of steps, undefined direction")
    print("c.positive(num_steps) ---------> Moves the carousel num_steps steps in the positive direction (Counterclockwise)")
    print("c.negative(num_steps) ---------> Moves the carousel num_steps steps in the negative direction (Clockwise)")
