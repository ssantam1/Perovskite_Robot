'''

Created by Pierce Alvir and Steven Santamorena

'''
import time
import board
import RPi.GPIO as GPIO

# These are how to instantiate x, y, and z
#x = axis(18,23,24,1200,0.001)
#y = axis(12,5,6,4800,0.0005)
#z = axis(16,20,21,3400,0.0008)
    
class Axis():
    def __init__(self, step_pin: int, dir_pin: int, en_pin: int, limit: int, sleep_var: float):
        self.steps_per_rev = 200 # Number of steps per revolution on stepper motor
        self.step_sleep_time = 0.001 # Time to sleep in between turning on and off GPIO for steps
        
        self.pos = 0
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        self.limit = limit
        self.sleep_var = sleep_var
        
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
            time.sleep(self.sleep_var)

    def positive(self, steps: int):
        GPIO.output(self.dir_pin, 1)
        self.move_steps(steps)
        self.pos += steps

    def negative(self, steps: int):
        GPIO.output(self.dir_pin, 0)
        self.move_steps(steps)
        self.pos -= steps

    
if __name__ == "__main__":
    x = Axis(18,23,24,1200,0.001)
    y = Axis(12,5,6,4800,0.0005)
    z = Axis(16,20,21,3400,0.0008)
    while(True):
        print(f"pos{x.pos}")
        cmd = "x."+input(">> ")
        try:
            exec(cmd)
        except Exception as E:
            print(f"Error {E}, try again.")
