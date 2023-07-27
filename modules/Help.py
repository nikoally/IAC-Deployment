import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

class TabModule(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Button 1
        self.help_button_1 = ttk.Button(self, text="Help Link 1",
                                        command=lambda: webbrowser.open('http://example.com/help1'))
        self.help_button_1.pack(side="top", padx=10, pady=10)

        # Button 2
        self.help_button_2 = ttk.Button(self, text="Help Link 2",
                                        command=lambda: webbrowser.open('http://example.com/help2'))
        self.help_button_2.pack(side="top", padx=10, pady=10)

        # Button 3
        self.help_button_3 = ttk.Button(self, text="Help Link 3",
                                        command=lambda: webbrowser.open('http://example.com/help3'))
        self.help_button_3.pack(side="top", padx=10, pady=10)

        # Button 4
        self.help_button_4 = ttk.Button(self, text="Help Link 4",
                                        command=lambda: webbrowser.open('http://example.com/help4'))
        self.help_button_4.pack(side="top", padx=10, pady=10)

