import time 
import board
import RPi.GPIO as GPIO

class Head():
    '''Class that represents the pipette inside the Perovskite Synthesis System'''

    def __init__(self):
        '''Constructs pipette object, configures GPIO pins'''
        # GPIO pin numbers
        self.step_pin = 13
        self.dir_pin = 19
        self.en_pin = 26
        self.vacuum_pin = 25

        # Stepper motor settings
        self.steps_per_rev = 800 # Num steps per revolution on stepper motor (200 x 4 from microstepping)
        self.steps_per_uL = 150/200 # Num steps per microliter
        self.step_sleep_time = 0.05 # Time to sleep in between turning on and off GPIO for steps
        
        # Limits and other things
        self.uL_correction = 0.925 # Correction factor for desired uL (set to 0 and run a series of tests to recalibrate)
        self.max_uL = 200 # Maximum volume of pipette
        self.limit = 275 # How many steps to move to lower the suction cup
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.output(self.en_pin, 0)

    # General motor movement functions

    def move_steps(self, steps: int):
        '''Moves the stepper a number a steps, does not change dir pin'''
        print(f"Moving {steps} steps")
        for _ in range(steps):
            GPIO.output(self.step_pin,1)
            time.sleep(0.0003)
            
            GPIO.output(self.step_pin,0)
            time.sleep(0.01)

    def down(self, steps: int):
        '''Moves the pipette plunger down a number of steps'''
        GPIO.output(self.dir_pin, 1)
        self.move_steps(steps)
        
    def up(self, steps: int):
        '''Moves the pipette plunger up a number of steps'''
        GPIO.output(self.dir_pin, 0)
        self.move_steps(steps)

    # Pipette actuation functions
        
    def down_uL(self, uL: int):
        '''Moves the pipette plunger down a number of microliters'''
        uL = uL * self.uL_correction
        steps = int(self.steps_per_uL * uL)
        self.down(steps)
        
    def up_uL(self, uL: int):
        '''Moves the pipette plunger up a number of microliters'''
        uL = uL * self.uL_correction
        steps = int(self.steps_per_uL * uL)
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
