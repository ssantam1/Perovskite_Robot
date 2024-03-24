import tkinter as tk
from tkinter import ttk

def submit_inputs():
    # Get the values from the input fields and do something with them
    pass

root = tk.Tk()

solution_frame = ttk.LabelFrame(root, text="Solution Selection")
solution_frame.grid(column=0, row=0, padx=10, pady=10, sticky="w")

solution1_var = tk.StringVar()
solution1_entry = ttk.Entry(solution_frame, width=5, textvariable=solution1_var)
solution1_entry.grid(column=0, row=0, padx=5, pady=5)

solution2_var = tk.StringVar()
solution2_entry = ttk.Entry(solution_frame, width=5, textvariable=solution2_var)
solution2_entry.grid(column=1, row=0, padx=5, pady=5)

solution3_var = tk.StringVar()
solution3_entry = ttk.Entry(solution_frame, width=5, textvariable=solution3_var)
solution3_entry.grid(column=2, row=0, padx=5, pady=5)

spin_coater_frame = ttk.LabelFrame(root, text="Spin Coater")
spin_coater_frame.grid(column=0, row=1, padx=10, pady=10, sticky="w")

speed_labels = [ttk.Label(spin_coater_frame, text=f"Speed {i+1}:" ) for i in range(3)]
duration_labels = [ttk.Label(spin_coater_frame, text=f"Duration {i+1}:" ) for i in range(3)]

for i in range(3):
    speed_labels[i].grid(column=0, row=i, padx=5, pady=5, sticky="w")
    duration_labels[i].grid(column=1, row=i, padx=5, pady=5, sticky="w")

speed_vars = [tk.StringVar() for _ in range(3)]
duration_vars = [tk.StringVar() for _ in range(3)]

for i in range(3):
    speed_entry = ttk.Entry(spin_coater_frame, width=5, textvariable=speed_vars[i])
    speed_entry.grid(column=2, row=i, padx=5, pady=5)
    duration_entry = ttk.Entry(spin_coater_frame, width=5, textvariable=duration_vars[i])
    duration_entry.grid(column=3, row=i, padx=5, pady=5)

hot_plate_frame = ttk.LabelFrame(root, text="Hot Plate")
hot_plate_frame.grid(column=0, row=2, padx=10, pady=10, sticky="w")

hot_plate_var = tk.StringVar()
hot_plate_entry = ttk.Entry(hot_plate_frame, width=5, textvariable=hot_plate_var)
hot_plate_entry.grid(column=0, row=0, padx=5, pady=5)

antisolvent_frame = ttk.LabelFrame(root, text="Antisolvent")
antisolvent_frame.grid(column=0, row=3, padx=10, pady=10, sticky="w")

dispense_time_var = tk.StringVar()
dispense_time_entry = ttk.Entry(antisolvent_frame, width=5, textvariable=dispense_time_var)
dispense_time_entry.grid(column=0, row=0, padx=5, pady=5)

volume_var = tk.StringVar()
volume_entry = ttk.Entry(antisolvent_frame, width=5, textvariable=volume_var)
volume_entry.grid(column=1, row=0, padx=5, pady=5)

submit_button = ttk.Button(root, text="Submit", command=submit_inputs)
submit_button.grid(column=0, row=4, padx=10, pady=10)

root.mainloop()
