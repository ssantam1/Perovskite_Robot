'''

Robotic Head Class File

Created by Pierce Alvir and Steven Santamorena

Usage: Class to operate robotic head mounted on the gantry

'''
import time 
import board
import RPi.GPIO as GPIO
import constants

class Head():
    '''Class that represents the pipette inside the Perovskite Synthesis System'''

    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = HEAD_STEP_PIN
        dir_pin = HEAD_DIR_PIN
        en_pin = HEAD_EN_PIN
        limit = limit if limit else HEAD_LIMIT
        step_delay = step_delay if step_delay else HEAD_STEP_DELAY
        microstep_mode = microstep_mode if microstep_mode else HEAD_MICROSTEP_MODE
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay, microstep_mode)
        vacuum_pin = HEAD_VACUUM_PIN
        

    def down(self, steps: int):
        '''Moves the pipette plunger down a number of steps'''
        self.positive(steps)
        
    def up(self, steps: int):
        '''Moves the pipette plunger up a number of steps'''
        self.negative(steps)

    # Pipette actuation functions
        
    def down_uL(self, uL: int):
        '''Moves the pipette plunger down a number of microliters'''
        uL = uL * HEAD_CORRECTION
        steps = int(HEAD_STEPS_PER_UL * uL)
        self.down(steps)
        
    def up_uL(self, uL: int):
        '''Moves the pipette plunger up a number of microliters'''
        uL = uL * HEAD_CORRECTION
        steps = int(HEAD_STEPS_PER_UL * uL)
        self.up(steps)
    
    # Suciton cup functions

    def lower_cup(self):
        '''Lowers the suction cup to below pipette tip'''
        self.down(self.limit)

    def raise_cup(self):
        '''Raises the suction cup to above pipette tip'''
        self.up(self.limit)

    def vac_on(self):
        '''Turns on the vacuum pump'''
        GPIO.output(self.vacuum_pin, 1)

    def vac_off(self):
        '''Turns off the vacuum pump'''
        GPIO.output(self.vacuum_pin, 0)

    # Motor power settings for live manipulation
        
    def enable(self):
        '''Enables the motor to move the pipette'''
        GPIO.output(self.en_pin, 0)
        
    def disable(self):
        '''Disables the motor to prevent movement'''
        GPIO.output(self.en_pin, 1)

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
