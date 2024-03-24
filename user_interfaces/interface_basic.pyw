from tkinter import *
from tkinter import ttk

def new_combobox(frame: Frame, values: list[str], coords: tuple[int,int], pad: tuple[int,int] = (5,5)) -> ttk.Combobox:
    row, column = coords
    padx, pady = pad

    combo = ttk.Combobox(frame, value=values)
    combo.current(0)
    combo.grid(row=row, column=column, sticky="e", padx=padx, pady=pady)
    return combo

def new_entrybox(frame: Frame, func, coords: tuple[int,int], pad: tuple[int,int] = (5,5)) -> Entry:
    row, column = coords
    padx, pady = pad

    entry = Entry(frame)
    entry.grid(row=row, column=column, padx=padx, pady=pady)
    entry.insert(0, "0")
    entry.bind("<KeyRelease>", func)
    return entry

def show_window():

    def safeInt(string: str) -> int:
        try:
            retval = int(string)
        except:
            retval = 0
        return retval

    def update_remaining( _ ):
        total = 100
        entry_values = [safeInt(entry1.get()), safeInt(entry2.get()), safeInt(entry3.get())]
        remaining = total - sum(entry_values)

        if remaining < 0:
            label_remaining.config(text=f"Remaining: {remaining}%", fg="red")
        elif remaining == 0:
            label_remaining.config(text=f"Remaining: {remaining}%", fg="green")
        else:
            label_remaining.config(text=f"Remaining: {remaining}%", fg="black")

    root = Tk()
    root.title("Perovskite Fabricatior")
    master = Frame(root, padx=10, pady=10)
    #root.geometry("500x400")

    solution_frame = Frame(master, borderwidth=5, relief=RAISED)

    # Column titles
    solution_label = Label(solution_frame, text="Selected Solutions")
    solution_label.grid(row=0, column=0, padx=5)
    percentage_label = Label(solution_frame, text="Percentage of Mix")
    percentage_label.grid(row=0, column=1, padx=5)

    solution_names = ["Solution A", "Solution B", "Solution C", "Solution D", "Solution E", "Solution F"]

    new_combobox(solution_frame, solution_names, (1,0))
    entry1 = new_entrybox(solution_frame, update_remaining, (1,1))

    new_combobox(solution_frame, solution_names, (2,0))
    entry2 = new_entrybox(solution_frame, update_remaining, (2,1))

    new_combobox(solution_frame, solution_names, (3,0))
    entry3 = new_entrybox(solution_frame, update_remaining, (3,1))

    # Display remaining percentage to allocate
    label_remaining = Label(solution_frame, text="Remaining: 100%")
    label_remaining.grid(row=4, columnspan=2)

    Label(master, text="Solution Selection", font="Default 13", relief=GROOVE).grid(column=0, row=0)
    solution_frame.grid(column=0, row=1, padx=5, pady=5)

    #======================================
    #  SPIN COATER FRAME

    spin_coater_frame = Frame(master, borderwidth=5, relief=RAISED)

    Label(spin_coater_frame, text="Step").grid(row=0, column=0, padx=5)
    Label(spin_coater_frame, text="Speed").grid(row=0, column=1, padx=5)
    Label(spin_coater_frame, text="Duration").grid(row=0, column=2, padx=5)

    Label(spin_coater_frame, text="#1").grid(row=1, column=0)
    Label(spin_coater_frame, text="#2").grid(row=2, column=0)
    Label(spin_coater_frame, text="#3").grid(row=3, column=0)

    new_entrybox(spin_coater_frame, None, (1,1))
    new_entrybox(spin_coater_frame, None, (2,1))
    new_entrybox(spin_coater_frame, None, (3,1))

    new_entrybox(spin_coater_frame, None, (1,2))
    new_entrybox(spin_coater_frame, None, (2,2))
    new_entrybox(spin_coater_frame, None, (3,2))

    Label(master, text="Spin Coater Steps", font="Default 13", relief=GROOVE).grid(column=1, row=0)
    spin_coater_frame.grid(column=1, row=1, padx=5, pady=5, sticky=NS)


    #======================================
    #  HOT PLATE FRAME      

    hot_plate_frame = Frame(master, borderwidth=5, relief=RAISED)

    bake_time_label = Label(hot_plate_frame, text="Bake time (Seconds)")
    bake_time_label.grid(row=0, column=0)

    bake_temp_label = Label(hot_plate_frame, text="Bake temp (Celcius)")
    bake_temp_label.grid(row=1, column=0)

    bake_time_entry = new_entrybox(hot_plate_frame, None, (0,1))
    bake_temp_entry = new_entrybox(hot_plate_frame, None, (1,1))

    Label(master, text="Hot Plate Options", font="Default 13", relief=GROOVE).grid(column=0, row=2)
    hot_plate_frame.grid(column=0, row=3, padx=5, pady=5, sticky=NS)

    #========================================
    #  DESOLVENT FRAME

    desolvent_frame = Frame(master, borderwidth=5, relief=RAISED)

    desolvent_time_label = Label(desolvent_frame, text="Dispense time")
    desolvent_time_label.grid(row=0, column=0)

    desolvent_vol_label = Label(desolvent_frame, text="Volume (uL)")
    desolvent_vol_label.grid(row=1, column=0)

    desolvent_time_entry = new_entrybox(desolvent_frame, None, (0,1))
    desolvent_vol_entry = new_entrybox(desolvent_frame, None, (1,1))

    Label(master, text="Antisolvent", font="Default 13", relief=GROOVE).grid(column=1, row=2)
    desolvent_frame.grid(column=1, row=3, padx=5, pady=5, sticky=NS)

    master.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    show_window()