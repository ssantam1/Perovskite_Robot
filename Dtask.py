'''

Procedure Generation File

Authors: ECD 415
         Pierce Alvir - Project Lead (CoE)
         Nicholas Blanchard - Mechanical Lead (ME)
         Steven Santamorena - Software Lead (CoE)
         Matthew Scott - Integration and Test Lead (ME)
         Luis Wang - Electrical Lead (EE)

Usage: robot task defs to use in main procedure

'''

import time
import constants as const
import drivers.axis as axis
from drivers.head import Head
from drivers.carousel import Carousel
from drivers.spincoater import SpinCoater
from drivers.hotplate import HotPlate

__author__ = "ECD415"
__version__ = "1.01"

# Create instances of the objects 
x_axis = axis.XAxis()
y_axis = axis.YAxis()
z_axis = axis.ZAxis()
gantry = axis.Gantry(y_axis, x_axis, z_axis)
head = Head()
carousel = Carousel(microstep_mode=4)
spincoater = SpinCoater()
hotplate = HotPlate()

# Establish USB connection to spin coater
spincoater.connect()


'''
ROBOT TASKS
'''

# Functions for Pipette Tip
def tip_on(increments: tuple[int, int]) -> int:
    '''
    pick up a dispenser tip
    increments: tuple[int, int] - (x, y) tip location in the tip rack
    (0, 0) is the top left when looking from the front of the machine
    '''
    increment_x, increment_y = increments
    y_coord, x_coord, z_coord = const.PIP_TO_TIP
    x_offset = 45
    y_offset = 56 * const.Y_MICROSTEP  # Multiplied for microstepping.
    # The new y and x coordinates will be based off of the starting coordinate subtracted/added to the offset * the increment.
    y_coord = y_coord - y_offset * increment_y 
    x_coord = x_coord + x_offset * increment_x
    gantry.go_to((y_coord, x_coord, z_coord), True)
    
    # If-else statements to stay within the tip pick up array
    if (increment_x > 11):
        increment_x = 0
        increment_y += 1
    else:
        increment_x += 1
        
    return increment_x, increment_y  # Return the next coming increments for reuse of function
    
def tip_off():
    '''Dispose of a tip'''
    gantry.go_to(const.DISPOSE_BIN, True)
    y_axis.go_home()
    z_axis.up(800)
    time.sleep(0.1)
    z_axis.down(800)
    y_axis.inward(100)

def wash_tip():
    extract_from_vial(head.max_uL, const.VIAL_CLEANER)
    gantry.go_to(const.DISPOSE_BIN, True)
    head.empty()
    gantry.home()

def go_to_vial():
    '''Moves the gantry to position the pipette tip above the active vial.'''
    (current_y, current_x, _) = gantry.get_coords()
    (target_y, target_x, _) = const.PIP_TO_VIAL

    already_at_vial: bool = current_y == target_y and current_x == target_x

    gantry.go_to(const.PIP_TO_VIAL, not already_at_vial)
    # Consider adding carousel.move_to_vial() here...
    # ...every call to this function calls it immediately after

def extract(uL: int):
    head.down_uL(head.max_uL)  # Empty air from pipette
    z_axis.down(1900)  # Lower pipette into vial
    head.up_uL(uL)  # Fill pipette with fluid
    time.sleep(0.25)
    z_axis.up(1900)  # Raise pipette above vial again

def extract_from_vial(uL, vial_num):
    go_to_vial()
    carousel.move_to_vial(vial_num)
    extract(uL)

def dispense_in_vial(vial_num):
    go_to_vial()
    carousel.move_to_vial(vial_num)
    z_axis.down(1000)  # Lower pipette into vial
    head.empty()
    z_axis.up(1000)

def mix_vial(vial_num):
    go_to_vial()
    carousel.move_to_vial(vial_num)
    z_axis.down(1900)
    for _ in range(3):
        head.empty()
    z_axis.up(1900)

# Functions for Spin Coater Stage
def get_slide():
    gantry.go_to(const.SLIDE_HOLDER, True)
    head.lower_cup()
    head.vac_on()
    head.raise_cup()

def drop_slide_to_spin():
    gantry.go_to(const.CUP_TO_SPIN, True)
    head.vac_off()
    head.lower_cup()
    time.sleep(3)
    head.raise_cup()

def retrieve_slide_from_spin():
    gantry.go_to(const.CUP_TO_SPIN, True)
    head.lower_cup()
    head.vac_on()
    head.raise_cup()

def go_to_hot():
    (curr_y, curr_x, curr_z) = gantry.get_coords()
    (targ_y, targ_x, targ_z) = const.CUP_TO_HOT
    if (curr_y == targ_y and curr_x == targ_x):
        gantry.go_to(const.CUP_TO_HOT, False)
    else:
        gantry.go_to(const.CUP_TO_HOT, True)

def slide_to_hot():
    go_to_hot()
    head.vac_off()
    head.lower_cup()
    time.sleep(3)
    head.raise_cup()

def retrieve_slide_from_hot():
    go_to_hot()
    z_axis.down(80)
    head.lower_cup()
    head.vac_on()
    head.raise_cup()
    z_axis.up(80)

def slide_return():
    gantry.go_to(const.TEMP_SLIDE_BIN, True)
    head.lower_cup()
    head.vac_off()
    time.sleep(3)
    head.raise_cup()

