'''

Created by Pierce Alvir and Steven Santamorena hi

'''
from drivers.axis import Axis

# Function for keeping track and performing xyz movement    
def xyz(x: Axis, y: Axis, z: Axis, x_coord: int, y_coord: int, z_coord: int):
    
    if (x_coord > x.limit or x_coord < 0):
        print(f"Error")
    elif (x_coord > x.pos):
        x_temp = x_coord-x.pos
        x.positive(x_temp)
    else:
        x_temp = x.pos-x_coord
        x.negative(x_temp)

    if (y_coord > y.limit or y_coord < 0):
        print(f"Error")
    elif (y_coord > y.pos):
        y_temp = y_coord-y.pos
        y.positive(y_temp)
    else:
        y_temp = y.pos-y_coord
        y.negative(y_temp)

    if (z_coord > z.limit or z_coord < 0):
        print(f"Error")
    elif (z_coord > z.pos):
        z_temp = z_coord-z.pos
        z.positive(z_temp)
    else:
        z_temp = z.pos-z_coord
        z.negative(z_temp)

    return (x,y,z)

# Function for pipette tip pick up

# Function for pipette tip ejection

# Function for antisolvent pick up

# Function for slide pick up
