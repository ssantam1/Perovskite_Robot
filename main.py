"""

Procedure Generation File
Created by Pierce Alvir and Steven Santamorena

"""
import time

import constants as const
import drivers.axis as axis
from drivers.head import Head
from drivers.carousel import Carousel
from drivers.spincoater import SpinCoater
from drivers.hotplate import HotPlate

__all__ = ['procedure']
__author__ = "Pierce Alvir and Steven Santamorena"
__version__ = "1.0"

# Create instances of the objects 
x_axis = axis.XAxis()
y_axis = axis.YAxis()
z_axis = axis.ZAxis()
gantry = axis.Gantry(y_axis, x_axis, z_axis)
head = Head()
carousel = Carousel(microstep_mode=4)
spincoater = SpinCoater()
hotplate = HotPlate()

# Functions for Pipette Tip
def tip_on(increments: tuple[int, int]) -> int:
    """
    increments: tuple[int, int] - (x, y) tip location in the tip rack
    (0, 0) Is the top left when looking from the front of the machine
    """
    increment_x, increment_y = increments
    y_coord, x_coord, z_coord = const.PIP_TO_TIP
    x_offset = 45
    y_offset = 56 * const.Y_MICROSTEP  # Multiplied for microstepping
    y_coord = y_coord - y_offset * increment_y
    x_coord = x_coord + x_offset * increment_x
    gantry.go_to((y_coord, x_coord, z_coord), True)
    
    if (increment_x > 11):
        increment_x = 0
        increment_y += 1
    else:
        increment_x += 1
        
    return increment_x, increment_y
    
def tip_off():
    '''Dispose of a tip'''
    gantry.go_to(const.DISPOSE_BIN, True)  # Need this for washing stage
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

# Functions for Carousel Stage
def go_to_vial():
    (curr_y, curr_x, curr_z) = gantry.get_coords()
    (targ_y, targ_x, targ_z) = const.PIP_TO_VIAL
    if (curr_y == targ_y and curr_x == targ_x):
        gantry.go_to(const.PIP_TO_VIAL, False)
    else:
        gantry.go_to(const.PIP_TO_VIAL, True)

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

# Actual Procedure Code to be used in GUI
def procedure(
    solutions: list[tuple[int, int]], 
    steps: list[tuple[int, int]], 
    hot_time: int, 
    antisolvent: tuple[int, int]):
    """
    solutions: list[(vial_num, percentage_mix)]
    steps: list[(rpm, time)]
    hot_time: bake time in seconds for hot plate
    antisolvent: (dispense_time, volume)
    """
    if len(solutions) != 3:
        raise ValueError("Must select 3 solutions.")
    
    if len(steps) != 3:
        raise ValueError("Must select 3 steps.")

    gantry.home()
    tip_increment = (0, 0)  # Keeping track of tip location
    tip_increment = tip_on(tip_increment)

    # Carousel Stage
    for sol in solutions:
        vial_num, percentage_mix = sol

        if percentage_mix == 0:
            continue

        print(f"sol: {sol}")

        vial_num += 1  # Gui handles vial nums starting at 0
        
        volume = percentage_mix / 100 * 2000
        print(f"Volume: {volume}")

        while volume > 0:
            to_extract = min(volume, 200)

            print(f"Doing extract_from_vial({to_extract}, {vial_num})...")
            extract_from_vial(to_extract, vial_num)
            volume -= to_extract

            print(f"Doing dispense_in_vial({const.VIAL_EMPTY_A})...")
            dispense_in_vial(const.VIAL_EMPTY_A)
        wash_tip()
    mix_vial(const.VIAL_EMPTY_A)  # You already have mixture taken in
    
    # Spin Coater Stage
    spincoater.connect()
    get_slide()
    drop_slide_to_spin()  # Needs to be written, but drop slide in spin coater
    gantry.go_to(const.PIP_TO_SPIN, True)
    head.empty()
    anti_disp_time, anti_vol = antisolvent  # Use antisolvent inputs
    extract_from_vial(anti_vol, const.VIAL_ANTISOLVENT)
    carousel.move_to_vial(1)
    total_spin_time = 0
    for spin_step in steps:
        rpm, spin_time = spin_step
        spincoater.add_step(rpm, spin_time)
        total_spin_time += spin_time
    gantry.go_to(const.PIP_TO_SPIN, True)
    start_time = time.perf_counter()
    current_time = 0
    spincoater.run()
    while(current_time < anti_disp_time):
        current_time = time.perf_counter() - start_time
    head.empty()
    time.sleep(total_spin_time - anti_disp_time)
    
    tip_off()
    spincoater.delete_steps()  # For future runs, delete steps off spin coater
    gantry.home()  # Recalibrate between stages again
    
    # Hot Plate Stage
    retrieve_slide_from_spin()
    hotplate.heat_up()
    slide_to_hot()  # Need to write but bring slide to hot plate
    hotplate.anneal(hot_time)
    retrieve_slide_from_hot()  # Maybe?
    slide_return()