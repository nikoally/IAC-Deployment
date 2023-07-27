import json
import pandas as pd
import os
import tkinter as tk
from tkinter import ttk

class CustomOptionMenu(tk.OptionMenu):
    def __init__(self, master, variable, *values, command=None):
        self._command = command
        self.variable = variable
        self.variable.trace("w", self._update_value)
        self._text = tk.StringVar()
        tk.OptionMenu.__init__(self, master, self._text, *values, command=self._command_stub)
        self._update_value()

    def _update_value(self, *args):
        value = self.variable.get()
        self._text.set(value)

    def _command_stub(self, value):
        if self._command is not None:
            self._command(value)

class TabModule(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.entries = {}
        
        with open("IAC-Deployment/static/cyberform.json", "r") as f:  # Use your actual JSON file path
            self.data = json.load(f)
        
        row = 0
        for category, questions in self.data['Categories'].items():
            for qid, question_data in questions.items():
                tk.Label(self, text=question_data['Question'], wraplength=600).grid(row=row, column=0, sticky="w")
                
                self.entries[qid] = tk.StringVar()
                choices = list(question_data['Answers'].keys())
                CustomOptionMenu(self, self.entries[qid], *choices).grid(row=row, column=1)
                row += 1
        
        tk.Button(self, text="Submit", command=self.submit).grid(row=row, column=0, columnspan=2)

    def submit(self):
        company_name = "Company"  # Use an actual company name or ask it from the user
        output_dir = f'output/{company_name}'
        os.makedirs(output_dir, exist_ok=True)

        records = []
        for category, questions in self.data['Categories'].items():
            for qid, question_data in questions.items():
                answer = self.entries[qid].get()
                records.append({'Category': category, 'QuestionID': qid, 'Answer': answer})

        # Save records to CSV
        csv_path = os.path.join(output_dir, 'results.csv')
        df = pd.DataFrame(records)
        df.to_csv(csv_path, index=False)
        
        # Call analyze_results function from analysis.py ***************

        # Clear the form
        for entry in self.entries.values():
            entry.set('')
