'''

Created by Pierce Alvir and Steven Santamorena

'''
from drivers.axis import *

#x = axis(18,23,24,1200,0.001)
#y = axis(12,5,6,4800,0.0005)
#z = axis(16,20,21,3400,0.0008)
    
def xyz(x: axis(), y: axis(), z: axis(), x_coord: int, y_coord: int, z_coord: int):
    
    if (x_coord > x.limit || x_coord < 0)
        print(f"Error")
    elif (x_coord > x.pos)
        x_temp = x_coord-x.pos
        x.positive(x_temp)
    else
        x_temp = x.pos-x_coord
        x.negative(x_temp)

    if (y_coord > y.limit || y_coord < 0)
        print(f"Error")
    elif (y_coord > y.pos)
        y_temp = y_coord-y.pos
        y.positive(y_temp)
    else
        y_temp = y.pos-y_coord
        y.negative(y_temp)

    if (z_coord > z.limit || z_coord < 0)
        print(f"Error")
    elif (z_coord > z.pos)
        z_temp = z_coord-z.pos
        z.positive(z_temp)
    else
        z_temp = z.pos-z_coord
        z.negative(z_temp)
