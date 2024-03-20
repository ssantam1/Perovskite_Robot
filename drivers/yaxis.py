import time
import board
import RPi.GPIO as GPIO

class Yaxis():
    # GPIO pin definitions
    step_pin = 12
    dir_pin = 5
    en_pin = 6

    def __init__(self):
        self.steps_per_rev = 200 # Number of steps per revolution on stepper motor
        self.step_sleep_time = 0.001 # Time to sleep in between turning on and off GPIO for steps
        
        self.pos = 0
        self.limit = 4800
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.output(self.en_pin,0)

    def move_steps(self, steps: int):
        print(f"Moving {steps} steps")
        for _ in range(steps):
            GPIO.output(self.step_pin, 1)
            time.sleep(0.0005)

            GPIO.output(self.step_pin, 0)
            time.sleep(0.0005)

    def inward(self, steps: int):
        GPIO.output(self.dir_pin, 0)
        self.move_steps(steps)
        self.pos -= steps

    def outward(self, steps: int):
        GPIO.output(self.dir_pin, 1)
        self.move_steps(steps)
        self.pos += steps
        
    def positive(self, steps: int):
        self.inward(steps)
        
    def negative(self, steps: int):
        self.outward(steps)
        
if __name__ == "__main__":
    y = Yaxis()
    while(True):
        print(f"pos{y.pos}")
        cmd = "y."+input(">> ")
        try:
            exec(cmd)
        except Exception as E:
            print(f"Error {E}, try again.")
            
