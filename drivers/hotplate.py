'''

Hot Plate Class File

Created by Pierce Alvir and Steven Santamorena

Usage: Class to control the hot plate and maybe include timing functions

'''

import time
import board
import RPi.GPIO as GPIO
from constants import *

class HotPlate():
    '''Class that represents the hot plate'''
    def __init__(self):
        self.en_pin = HOTPLATE_EN_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.en_pin, GPIO.OUT)
    
    def hot_on(self): #not sure if on is output high or low 
        GPIO.output(self.en_pin,0)

    def hot_off(self):
        GPIO.output(self.en_pin,1)

    def anneal(self, seconds_time: int): #we can rename the time variable
        start_time = time.perf_counter()
        while(seconds_time != current_time):
            hot_on()
            current_time = time.perf_counter()-start_time
        hot_off()

if __name__ == "__main__":
    plate = HotPlate()
    while(True):
        anneal(60) #turn hot plate on for a minute hopefully
