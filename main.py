'''

Procedure Generation File

Authors: ECD 415
         Pierce Alvir - Project Lead (CoE)
         Nicholas Blanchard - Mechanical Lead (ME)
         Steven Santamorena - Software Lead (CoE)
         Matthew Scott - Integration and Test Lead (ME)
         Luis Wang - Electrical Lead (EE)

Usage: Main procedure with additional helper functions

'''

import time

# Importing using wildcard "*" in bad practice.
# Instead, maybe "import Dtask as task"
# Then, tasks can be called like: task.wash_tip().
# Although, calling it task may be confusing...
# ...in the future if async processes are ever added
from Dtask import *

__all__ = ['procedure']
__author__ = "ECD415"
__version__ = "1.0"


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
    
    # Input validation:
    if len(solutions) != 3:
        raise ValueError("Must select 3 solutions.")
    
    if len(steps) != 3:
        raise ValueError("Must select 3 steps.")
        

    # Initialize sample prep cycle   

    # Send gantry to home position in case it is not already there
    gantry.home()
        
    # Get a pipette tip from the tip rack
    tip_increment = (0, 0)  # Keeping track of tip location
    tip_increment = tip_on(tip_increment)

    # Carousel Stage
    
    # dispense solutions in mixing vial
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
        
    # Mix the solution
    mix_vial(const.VIAL_EMPTY_A)
    dispense_in_vial(const.VIAL_EMPTY_A)
    
    
    # Spin Coater Stage
    
    #####   we could start heating up the hotplate here
    # heat_start = time.time()   # epoch
    # hotplate.on()   # new fcn
    
    # Pick up a slide and place in spincoater chuck
    get_slide()
    drop_slide_to_spin()
    
    # Get mixed solution and dispense on slide in chuck
    extract_from_vial(head.max_uL, const.VIAL_EMPTY_A)
    gantry.go_to(const.PIP_TO_SPIN, True)
    head.empty()
    
    # Load pipette with antisolvent
    anti_disp_time, anti_vol = antisolvent  # Use antisolvent inputs
    extract_from_vial(anti_vol, const.VIAL_ANTISOLVENT)
    carousel.move_to_vial(1)
    
    # Add steps to spincoater over serial connection,
    # and calculate total time spent spinning (needed for later)
    total_spin_time = 0
    for spin_step in steps:
        rpm, spin_time = spin_step
        spincoater.add_step(rpm, spin_time)
        total_spin_time += spin_time
        
    # Move pipette to coater    
    gantry.go_to(const.PIP_TO_SPIN, True)
    
    # Start spin, dispense antisolvent after delay and finish spin
    start_time = time.perf_counter()
    current_time = 0
    spincoater.run()
    while(current_time < anti_disp_time):
        current_time = time.perf_counter() - start_time
    
    # Dispense antisolvent...
    head.empty()
    # ...and wait for the spinning to finish
    time.sleep(total_spin_time - anti_disp_time)
    
    # Discard tip and send gantry home
    tip_off()
    spincoater.delete_steps()  # For future runs, delete steps off spin coater
    gantry.home()  # Recalibrate between stages again
    
    # Hot Plate Stage
    
    # Pick up slide from coater 
    retrieve_slide_from_spin()
    
    # Wait for hotplate to pre-heat to near 100c
    hotplate.heat_up()
    
    # Place slide on hot plate and anneal film
    slide_to_hot() 
    hotplate.anneal(hot_time)
    
    # Pick up slide from hot plate and transfer slide to storage
    retrieve_slide_from_hot()
    slide_return()