import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

file_path = filedialog.askopenfilename()

if file_path:
    print("Selected file:", file_path)