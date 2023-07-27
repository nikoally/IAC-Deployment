import tkinter as tk
from tkinter import ttk

class TabModule(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="This is Module 2")
        self.label.pack()
