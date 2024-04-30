import board
import RPi.GPIO as GPIO

from drivers.stepper import Stepper
from constants import *  # Should change to import as const for PEP 8.

class Carousel(Stepper):
    '''Class that represents the vial carousel inside the work area'''
    def __init__(self,
        step_delay: int = CAROUSEL_STEP_DELAY,
        microstep_mode: int = 1) -> None:
        '''
        Initializes the carousel stepper motor
        
        Args:
            step_delay (int, optional): Step delay for homeing process.
            microstep_mode (int, optional): Microstep factor. Default: 1
        '''
        super().__init__(CAROUSEL_STEP_PIN,
            CAROUSEL_DIR_PIN,
            CAROUSEL_EN_PIN,
            None, step_delay,
            microstep_mode=microstep_mode)

        self.steps_per_rev = 200 * microstep_mode  # Num steps/revolution.
        self.num_vials = 8  # Number of vials/slots in the carousel.
        self.current_vial = 1  # Current vial the carousel is at.

    def reset_vial(self):
        '''Tell the carousel that it is at vial 1'''
        # This is mainly so I can do tests without resetting the program.
        self.current_vial = 1

    def move_to_vial(self, target_vial: int) -> None:
        '''Moves the carousel to a desired vial'''

        # Check if the target vial is within the bounds of the carousel.
        if target_vial < 1 or target_vial > self.num_vials:
            raise Exception("""
                Vial numbers must be non-negative and not exceed num_vials-1
                """)

        # Calculate number of steps needed to move to the desired vial.
        steps_to_move = int(abs(target_vial - self.current_vial) * (self.steps_per_rev / self.num_vials))
 
        # Set the direction of the motor based on the target vial
        if target_vial > self.current_vial:
            GPIO.output(self.dir_pin,1)
        else:
            GPIO.output(self.dir_pin,0)

        # Move the motor to the target vial
        accel = CAROUSEL_ACCEL_CONST
        min_delay = CAROUSEL_MIN_DELAY
        self.move_smooth(steps_to_move, accel, min_delay)

        # Update the current vial
        self.current_vial = target_vial

if __name__ == "__main__":
    # Run with -i flag to test any functions of the carousel
    c = Carousel()