import tkinter as tk  # Imports the main Tkinter module
from tkinter import ttk, font, messagebox, PhotoImage


# Organizes all the functionality of the application
class TaskApp:
    def __init__(self, root):
        self.root = root  # Creates and assigns the main window
        self.task_entry = None
        self.canvas = None
        self.interior_canvas = None
        self.editing_frame = None  # Initializes the variable that will store the task being edited as None
        self.configure_window()  # Configures the main window
        self.create_widgets()  # Creates and positions the interface elements
        self.edit_icon = PhotoImage(file="edit-icon.png").subsample(30, 30)  # Creates and configures the edit button
        self.delete_icon = PhotoImage(file="delete-icon.png").subsample(30, 30)  # Creates and configure the delete button

    def configure_window(self):
        self.root.title("Task App")
        self.root.config(bg="#242424")

        # Set the size of the window
        window_width = 480
        window_height = 750

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(width=False, height=False)  # Prevents the window from being resized

    # Creates all the graphical components of the interface
    def create_widgets(self):
        # Header
        header_font = font.Font(family="Garamond", size=24, weight="bold")
        tk.Label(self.root, text="Task App", font=header_font, bg="#242424", fg="white").pack(pady=20)

        # Input where the user enters the text
        frame = tk.Frame(self.root, bg="#242424")
        frame.pack(pady=10)

        self.task_entry = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, bg="white", fg="grey", width=30)
        self.task_entry.pack(side=tk.LEFT, padx=10)

        # Add button
        add_button = tk.Button(frame, command=self.add_task, text="Add", bg="white", fg="black",
                               height=1, width=15, font=("Roboto", 11), relief=tk.FLAT)
        add_button.pack(side=tk.LEFT, padx=10)

        # Scrollable task list
        task_list_frame = tk.Frame(self.root, bg="black")
        task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(task_list_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Creates a vertical scrollbar
        scrollbar = tk.Scrollbar(task_list_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=scrollbar.set)
        self.interior_canvas = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.interior_canvas, anchor="nw")
        self.interior_canvas.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

    # Add a task to the list
    def add_task(self):
        task = self.task_entry.get().strip()  # Gets the text entered by the user and removes leading and trailing whitespace
        if task and task != "Write your task here":  # Checks if the task is not empty and is not the default text
            if self.editing_frame is not None:  # If a task is being edited, calls update_task
                self.update_task(task)
                self.editing_frame = None
            else:  # Otherwise, add the new task by calling add_task_item
                self.add_task_item(task)
                self.task_entry.delete(0, tk.END)
        else:
            tk.messagebox.showwarning("Invalid Input",
                                      "Please enter a task.")  # If the input is empty, display an alert with messagebox

    # Updates the task being edited
    def update_task(self, new_task):
        for widget in self.editing_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=new_task)

    # Prepares the editing of an existing task
    def prepare_edit(self, task_frame, task_label):
        self.editing_frame = task_frame
        self.task_entry.delete(0, tk.END)
        self.task_entry.insert(0, task_label.cget("text"))

    # Deletes the task
    def delete_task(self, task_frame):
        task_frame.destroy()
        self.interior_canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # Adds or removes the underline when clicking the checkbox
    @staticmethod
    def change_underline(label):
        current_font = label.cget("font")
        if "overstrike" in current_font:
            new_font = current_font.replace(" overstrike", "")
        else:
            new_font = current_font + " overstrike"
        label.config(font=new_font)

    def add_task_item(self, task):
        task_frame = tk.Frame(self.interior_canvas, bg="white", bd=1, relief=tk.SOLID)
        task_label = tk.Label(task_frame, text=task, font=("Garamond", 16,), bg="white", fg="black", width=25, height=2,
                              anchor="w")
        task_label.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
        edit_button = tk.Button(task_frame, image=self.edit_icon,
                                command=lambda f=task_frame, l=task_label: self.prepare_edit(f, l), bg="white",
                                relief=tk.FLAT)
        edit_button.pack(side=tk.RIGHT, padx=5)
        delete_button = tk.Button(task_frame, image=self.delete_icon,
                                  command=lambda f=task_frame: self.delete_task(f), bg="white", relief=tk.FLAT)
        delete_button.pack(side=tk.RIGHT, padx=5)
        task_frame.pack(fill=tk.X, padx=5, pady=5)
        checkbutton = tk.Checkbutton(task_frame,
                                     command=lambda label=task_label: self.change_underline(label), bg="white")
        checkbutton.pack(side=tk.RIGHT, padx=5)
        self.interior_canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


root = tk.Tk()  # Initializes the main window
app = TaskApp(root)  # Creates an instance of the application
root.mainloop()  # Starts the main loop of the interface
