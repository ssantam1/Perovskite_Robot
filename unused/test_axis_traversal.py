from drivers.xaxis import Xaxis
from drivers.yaxis import Yaxis
from drivers.zaxis import Zaxis
import time

# Create instances of the objects
x = Xaxis()
y = Yaxis()
z = Zaxis()

print("Please ensure axes are in their furthest left/down/out positions\n")

for axis in [z, y, x]:
	input(f"Press enter to begin {type(axis).__name__} traversal test ...")
	
	start = time.perf_counter()
	axis.positive(axis.limit)
	end = time.perf_counter()
	
	time.sleep(0.10)
	axis.negative(axis.limit)
	
	print(f"Done! Time: {(end-start):.2f} seconds\n")
