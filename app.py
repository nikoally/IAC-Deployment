import os
import tkinter as tk
from tkinter import ttk
import importlib.util

class Application(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand="true")
        self.load_modules()

    def load_modules(self):
        module_dir = os.path.join(os.path.dirname(__file__), "modules")
        for filename in os.listdir(module_dir): #Iterates over files in the modules dir and imports them
            if filename.endswith(".py"):
                module_name = filename[:-3]  # strip .py at the end
                module_path = os.path.join(module_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                tab = module.TabModule(self)
                self.add(tab, text=module_name) #Creates a tab for each module


root = tk.Tk()
app = Application(master=root)
app.mainloop()
