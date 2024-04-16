'''

Axis Classes File

Created by Pierce Alvir and Steven Santamorena

Usage: Axis Movement Helper Classes

'''
import time
import board
import RPi.GPIO as GPIO
from constants import *
from drivers.stepper import Stepper

class Axis(Stepper):
    def __init__(self, step_pin, dir_pin, en_pin, home_pin, limit, step_delay, flip_dir = False, microstep_mode = 1) -> None:
        super().__init__(step_pin, dir_pin, en_pin, limit, step_delay, flip_dir, microstep_mode)
        self.home_pin = home_pin
        # You can uncomment this line if you rewire the home switches to use less cabling
        #GPIO.setup(self.home_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.home_pin, GPIO.IN)

    def is_home(self):
        # Our switches are active low
        return not GPIO.input(self.home_pin)

    def go_home(self):
        print("Going home...")
        GPIO.output(self.dir_pin, 0 ^ self.flip_dir)
        while not self.is_home():
            self.move_steps(1)
            self.pos -= 1
        print(f"Homed! Steps lost: {self.pos}")
        self.pos = 0

class XAxis(Axis):
    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = X_STEP_PIN
        dir_pin = X_DIR_PIN
        en_pin = X_EN_PIN
        home_pin = X_HOME_PIN
        limit = limit if limit else X_LIMIT
        step_delay = step_delay if step_delay else X_STEP_DELAY
        super().__init__(step_pin, dir_pin, en_pin, home_pin, limit, step_delay, flip_dir=False, microstep_mode=microstep_mode)

    def positive(self, steps: int):
        self.accel_positive(steps, X_ACCEL_CONST, X_MIN_DELAY, X_MAX_DELAY)

    def negative(self, steps: int):
        self.accel_negative(steps, X_ACCEL_CONST, X_MIN_DELAY, X_MAX_DELAY)

    def right(self, steps: int):
        self.positive(steps)

    def left(self, steps: int):
        self.negative(steps)

class YAxis(Axis):
    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = Y_STEP_PIN
        dir_pin = Y_DIR_PIN
        en_pin = Y_EN_PIN
        home_pin = Y_HOME_PIN
        limit = limit if limit else Y_LIMIT
        step_delay = step_delay if step_delay else Y_STEP_DELAY
        super().__init__(step_pin, dir_pin, en_pin, home_pin, limit, step_delay, flip_dir=True, microstep_mode=microstep_mode)

    def positive(self, steps: int):
        self.accel_positive(steps, Y_ACCEL_CONST, Y_MIN_DELAY)

    def negative(self, steps: int):
        self.accel_negative(steps, Y_ACCEL_CONST, Y_MIN_DELAY)

    def inward(self, steps: int):
        self.positive(steps)

    def outward(self, steps: int):
        self.negative(steps)
        
class ZAxis(Axis):
    def __init__(self, limit: int = None, step_delay: int = None, microstep_mode: int = 1) -> None:
        step_pin = Z_STEP_PIN
        dir_pin = Z_DIR_PIN
        en_pin = Z_EN_PIN
        home_pin = Z_HOME_PIN
        limit = limit if limit else Z_LIMIT
        step_delay = step_delay if step_delay else Z_STEP_DELAY
        super().__init__(step_pin, dir_pin, en_pin, home_pin, limit, step_delay, flip_dir=False, microstep_mode=microstep_mode)

    def positive(self, steps: int):
        self.accel_positive(steps, Z_ACCEL_CONST, Z_MIN_DELAY, Z_MAX_DELAY)

    def negative(self, steps: int):
        self.accel_negative(steps, Z_ACCEL_CONST, Z_MIN_DELAY, Z_MAX_DELAY)

    def up(self, steps: int):
        self.negative(steps)

    def down(self, steps: int):
        self.positive(steps)

class Gantry():
    def __init__(self, y: YAxis, x: XAxis, z: ZAxis):
        self.x = x
        self.y = y
        self.z = z
    
    # Function for keeping track and performing xyz movement    
    def go_to(self, coord: tuple[int, int, int], obstacle_det: bool):
        '''
        coord: take in the coordinated desired via yxz
        obstacle_det: avoid any obstacles
        '''
        axis = (self.y,self.x,self.z)

        if obstacle_det:
            axis[2].go_home()

        axis_and_coords = [(axis[i], coord[i]) for i in range(len(axis))]

        '''
        (axis[1], coord[1]),
        (axis[2], coord[2]),
        (axis[3], coord[3])

        for (a, c) in axis_and_coords:
            a.positive(c)
            
        '''
            
        for i in range(3):
            if (coord[i] > axis[i].limit or coord[i] < 0):
                print(f"Error") # Pierce we really need a more descriptive error and also maybe throw an exception
                exit()
            elif (coord[i] > axis[i].pos):
                axis_temp = coord[i]-axis[i].pos
                axis[i].positive(axis_temp)
            else:
                axis_temp = axis[i].pos-coord[i]
                axis[i].negative(axis_temp)
        return axis
    
    def home(self):
        '''
        Homes all axes
        '''
        self.z.go_home()
        self.x.go_home()
        self.y.go_home()
    
    def get_coords(self):
        return (self.y.pos, self.x.pos, self.z.pos)