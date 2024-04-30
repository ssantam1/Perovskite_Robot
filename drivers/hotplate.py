'''

Hot Plate Class File

Created by Pierce Alvir and Steven Santamorena

Usage: Class to control the hot plate and maybe include timing functions

'''

import time

import board
import RPi.GPIO as GPIO

from constants import *  # Should change to import as const for PEP 8.

class HotPlate():
    '''Class that represents the hot plate'''
    def __init__(self):
        '''Constructs hot plate object, configures GPIO pins'''
        self.en_pin = HOTPLATE_EN_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.en_pin, GPIO.OUT)
        self.hot_off()
    
    def hot_on(self):
        '''Turns on the hot plate'''
        GPIO.output(self.en_pin,1)

    def hot_off(self):
        '''Turns off the hot plate'''
        GPIO.output(self.en_pin,0)

    def heat_up(self):
        '''Turns on the hot plate and waits for it to heat up'''
        self.hot_on()
        time.sleep(30) #sleep for 30 seconds to heat up

    def anneal(self, seconds_time: int):
        '''Only use anneal after the heat up function has been performed'''
        start_time = time.perf_counter()
        current_time = 0
        while(current_time < seconds_time):
            current_time = time.perf_counter()-start_time
        self.hot_off()

if __name__ == "__main__":
    # Run with -i flag to test in interactive mode
    plate = HotPlate()