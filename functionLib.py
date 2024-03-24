'''

Created by Pierce Alvir and Steven Santamorena

'''
from drivers.axis import *

# Function for keeping track and performing xyz movement    
def go_to(axis: tuple[YAxis, XAxis, ZAxis], coord: tuple[int, int, int], obstacle_det: bool):
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
            print("Going positive")
            axis_temp = coord[i]-axis[i].pos
            axis[i].positive(axis_temp)
        else:
            print("Going negative")
            axis_temp = axis[i].pos-coord[i]
            axis[i].negative(axis_temp)
    return axis

# Function for pipette tip pick up
def tip_on(incrementer: int) -> int:
    '''
    incrementer: stored variable in main file that knows what iteration to set the tip to
    function returns incrementer number as well
    '''
    
    zyx((z,y,x),(300,1308,13),True) #replace with constant coord

# Function for pipette tip ejection
def tip_off():
	'''
        ejects tip should be same for any time you want to take tip off

        maybe consider washing the tips instead of ejecting
        '''
	zyx((z,y,x),(1000,100,900),True)
	y.go_home()
	z.up(1400)
	z.down(1400)
	y.inward(100)
# Function for antisolvent pick up

# Function for slide pick up
