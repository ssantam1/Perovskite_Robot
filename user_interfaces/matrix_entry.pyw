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

    '''def update_remaining( _ ):
        total = 100
        entry_values = [safeInt(entry1.get()), safeInt(entry2.get()), safeInt(entry3.get())]
        remaining = total - sum(entry_values)

        if remaining < 0:
            label_remaining.config(text=f"Remaining: {remaining}%", fg="red")
        elif remaining == 0:
            label_remaining.config(text=f"Remaining: {remaining}%", fg="green")
        else:
            label_remaining.config(text=f"Remaining: {remaining}%", fg="black")'''

    root = Tk()
    root.title("Perovskite Fabricatior")
    #root.geometry("500x400")

    frame = Frame(root)
    frame.pack(padx=10, pady=10)

    # Column titles
    initial_label = Label(frame, text="Initial Solutions")
    initial_label.grid(row=1, column=0, padx=5)

    initial_label = Label(frame, text="Num of steps")
    initial_label.grid(row=2, column=0, padx=5)
    
    final_label = Label(frame, text="Final Solutions")
    final_label.grid(row=3, column=0, padx=5)
                        
    solution_label = Label(frame, text="AX")
    solution_label.grid(row=0, column=1, padx=5)
                        
    solution_label = Label(frame, text="BX2")
    solution_label.grid(row=0, column=2, padx=5)

    AX_names = ["Methylammonium iodide", "Formamidinium iodide", "Caesium iodide"]
    BX_names = ["Tin iodide", "Lead iodide"]

    new_combobox(frame, AX_names, (1,1))
    entry1 = new_entrybox(frame, None, (2,1))
    new_combobox(frame, AX_names, (3,1))

    new_combobox(frame, BX_names, (1,2))
    entry1 = new_entrybox(frame, None, (2,2))
    new_combobox(frame, BX_names, (3,2))

    # Display remaining percentage to allocate
    #label_remaining = Label(frame, text="Remaining: 100%")
    #label_remaining.grid(row=4, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    show_window()