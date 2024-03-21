'''

Created by Pierce Alvir and Steven Santamorena hi

'''
from drivers.axis import *

# Function for keeping track and performing xyz movement    
def zyx(axis: tuple[ZAxis, YAxis, XAxis], coord: tuple(int, int, int), obstacle_det: bool):
    if obstacle_det:
        zyx(axis, (3200, coord[2], coord[3]), false)

    axis_and_coords = [(axis[i], coord[i]) for i in range(len(axis))]

    '''
    (axis[1], coord[1]),
    (axis[2], coord[2]),
    (axis[3], coord[3])

    for (a, c) in axis_and_coords:
        a.positive(c)
        
    '''
        
    for i in range(3):
        if (coord[i] >axis[i].limit or coord[i] < 0):
            print(f"Error")
        elif (coord[i] > axis[i].pos):
            axis_temp = coord[i]-axis[i].pos
            axis[i].positive(axis_temp)
        else:
            axis_temp = axis[i].pos-coord[i]
            axis[i].negative(axis_temp)
    return (z,y,x)

# Function for pipette tip pick up

# Function for pipette tip ejection

# Function for antisolvent pick up

# Function for slide pick up
