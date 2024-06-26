'''

Spin Coater Class File

Authors: ECD 415
         Pierce Alvir - Project Lead (CoE)
         Nicholas Blanchard - Mechanical Lead (ME)
         Steven Santamorena - Software Lead (CoE)
         Matthew Scott - Integration and Test Lead (ME)
         Luis Wang - Electrical Lead (EE)

Usage: Class to control the spin coater over serial connection

'''
import time

import board
import RPi.GPIO as GPIO
from serial import Serial, SerialException

from constants import *  # Should change to import as const for PEP 8

class SpinCoater():
    '''Class that represents the spin coater inside the Perovskite Synthesis System'''

    def __init__(self):
        '''Constructs spin coater object, configures GPIO pins'''
        self.enable_pin = SPINCOATER_EN_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, 1)

        self.conn = None # Inits to None until connect() is called externally

    # Internal stuff, not intended to be called from outside

    def _connect(self, com_port) -> Serial:
        '''Connects to the spin coater board'''
        try:
            spc_serial_connection = Serial(com_port, baudrate=9600, timeout=None)
            if spc_serial_connection.is_open is False:
                raise Exception("Connection's is_open is False, connection failed.")
            else:
                return spc_serial_connection
        
        except SerialException as E:
            print(E)
            return None
        
    def _send_command(self, command: str) -> None:
        '''Sends a command to the spin coater board'''
        self.conn.write(command.encode("ascii"))

    def _board_return(self) -> str:
        '''Reads and returns the response from the spin coater board'''
        return_data = self.conn.read_all()
        return_data = return_data.decode('utf-8')
        return return_data
    
    def _send_and_return(self, command: str) -> str:
        '''Sends a command to the spin coater board and returns the response'''
        self._send_command(command)
        time.sleep(0.5)
        return self._board_return()
    
    # External API

    def connect(self):
        self.conn = self._connect("/dev/ttyACM0")
        if self.conn is None:
            print("Spin coater connection Failed, see exception above.")
            input("Press return to exit...")
            exit()

        data = self._send_and_return("spc set pcmode")
        print(f"Board returned: {data}")
    
    def add_step(self, rpm: int, time: int) -> str:
        '''Adds a step to the spin coater, returns the response from the board'''
        print(f"Adding step: {rpm}rpm, {time}seconds")
        return self._send_and_return(f"spc add step {rpm} {time}")
    
    def get_steps(self) -> str:
        '''Gets all steps from the spin coater, returns the response from the board'''
        stps = self._send_and_return("spc get steps")
        print(stps)
        return stps

    def delete_steps(self) -> str:
        '''Deletes all steps from the spin coater, returns the response from the board'''
        return self._send_and_return("spc del steps")

    def run(self):
        '''Runs the spin coater'''
        print(self._send_and_return("spc run"))

if __name__ == "__main__":
    # Run with -i flag to test any functions of the spincoater
    spc = SpinCoater()