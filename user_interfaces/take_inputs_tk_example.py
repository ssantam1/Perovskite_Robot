import tkinter as tk
#import pass_inputs_tk_example

def submit_callback():
    # Get the input from the tkinter Entry widget
    input_value = input_entry.get()
    # Call the main script and pass the input value as an argument
    progX(input_value)

# Create the tkinter window
window = tk.Tk()

# Create a tkinter label
tk.Label(window, text="Enter a value:").pack()

# Create a tkinter Entry widget
input_entry = tk.Entry(window)
input_entry.pack()

# Create a tkinter Button widget
submit_button = tk.Button(window, text="Submit", command=submit_callback)
submit_button.pack()

# Start the tkinter mainloop
window.mainloop()
