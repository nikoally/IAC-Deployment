# modules/data_processing.py
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dateutil.parser import parse as parse_datetime
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import json
import csv
import numpy as np

class TabModule(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        
        self.outputdict = {}
        self.friendly_names = []
        self.site_number = simpledialog.askinteger("Input", "Enter the site number:")
        self.load_directory()

    def select_file(self): 
        self.input_file = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        self.file_label = tk.Label(self, text=f"{os.path.basename(self.input_file)}")
        self.file_label.grid(row = 6, column = 1, sticky = "w")
    
    def clear_form(self):
        self.inputformheader = tk.Label(self, text = "Add Data to Site" )
        self.inputformheader.grid(row = 0, column = 1, sticky = "nsew")

        self.text_label = tk.Label(self, text="Enter Friendly Name")
        self.text_label.grid(row = 1, column = 1, sticky = "w")
        
        self.text_entry = tk.Entry(self)
        self.text_entry.grid(row = 2, column = 1, sticky = "w")

        self.number_label = tk.Label(self, text="Enter Wattage")
        self.number_label.grid(row = 3, column = 1, sticky = "w")
        
        self.number_entry = tk.Entry(self)
        self.number_entry.grid(row = 4, column = 1, sticky = "w")

        self.select_file_button = tk.Button(self, text="Select File", command=self.select_file)
        self.select_file_button.grid(row = 5, column = 1, sticky = "w")

        self.file_label = tk.Label(self, text="                                              ")
        self.file_label.grid(row = 6, column = 1, sticky = "w")
    
    def create_widgets(self):
        self.clear_form()
        self.submit_button = tk.Button(self, text="Submit", command=self.load_file)
        self.submit_button.grid(row=7, column=1, sticky="w")

        self.filelist_label = tk.Label(self, text="Currently Imported Files")
        self.filelist_label.grid(row=0, column=0, sticky="nsew")
        
        self.file_listbox = tk.Listbox(self)
        self.file_listbox.grid(row=1, rowspan=7, column=0, pady=10, padx=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.export_button = ttk.Button(self, text="Export", command=self.export_data)
        self.export_button.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

    def load_json(self):
        self.site_data = {}
        self.file_listbox.delete(0, tk.END)
        if os.path.isfile(f'{self.project_directory}/sitedata.json'):
            with open(f'{self.project_directory}/sitedata.json', 'r') as json_file:
                self.site_data = json.load(json_file)
                print(self.site_data.items())
            for path, items in self.site_data.items():
                print(path, items)
                self.file_listbox.insert(tk.END, "Name: " + items['friendly_name'] + f" Wattage: {items['wattage']}")
                print("Imported Site Data")
        else:
            print("No Site Data to Import ")

    def load_directory(self):
        self.project_directory = f"/Users/nicholasbailey/Documents/IAC-Database/{self.site_number}/Light-Occupancy"
        for folder in ["graphs", "data"]:
            if not os.path.exists(f'{self.project_directory}/{folder}'):
                os.makedirs(f'{self.project_directory}/{folder}')
                print(f"Created {folder} folder")
            else: 
                print(f"{folder} already exists")
        print(f"Project Directory: {self.project_directory}")
        
        # Import previous site data if it exists
        self.load_json()
        

    def load_file(self): #Command for submit button
        # Get form info
        wattage = self.number_entry.get()
        friendly_name = self.text_entry.get()

        # store the data in the dictionary
        file_data = {'friendly_name': friendly_name, 'wattage': wattage}
        print(file_data)
        # Read the csv file
        df = pd.read_csv(self.input_file, usecols=[0, 1, 2, 3])

        # Change column names to standardized names
        df.columns = ['Index', 'Timestamp', 'Light', 'Occupancy']

        # Drop the index column
        df = df.drop(columns=['Index'])

        # Convert Date Time to datetime and sort by it
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.sort_values('Timestamp', inplace=True)

        # Set Timestamp as index
        df.set_index('Timestamp', inplace=True)

        # Resample the dataframe to every second, forward fill missing data
        df = df.resample('S').ffill()
        df['Light'].fillna(method='ffill', inplace=True)
        df['Occupancy'].fillna(method='ffill', inplace=True)

    # Light on no Occ Time

        # Find the rows where Light is on (1.00) and Occupancy is off (0.00)
        df_light_on_no_occupancy = df[(df['Light'] == 1.00) & 
                                    (df['Occupancy'] == 0.00)]

        # Calculate the time difference between consecutive timestamps
        df_light_on_no_occupancy.loc[:, 'Time Difference'] = df_light_on_no_occupancy.index.to_series().diff().dt.total_seconds()


        # Sum up the total time
        total_time = df_light_on_no_occupancy['Time Difference'].sum()

        # Store total time
        file_data['total_time_light_on_no_occupancy'] = total_time
    
    #Light On, Occ On Time
    
        # Find the rows where Light is on (1.00) and Occupancy is off (0.00)
        df_light_on_with_occupancy = df[(df['Light'] == 1.00) & 
                                    (df['Occupancy'] == 1.00)]

        # Calculate the time difference between consecutive timestamps
        df_light_on_with_occupancy.loc[:, 'Time Difference'] = df_light_on_with_occupancy.index.to_series().diff().dt.total_seconds()


        # Sum up the total time
        total_time_on_occ = df_light_on_with_occupancy['Time Difference'].sum()

        # Store total time
        file_data['total_time_light_on'] = (total_time + total_time_on_occ)
          

        # Make new dataframe with minute resolution to save 
        df_60th = df.iloc[::60, :]
        
        # Save pd to csv
        df_60th.to_csv(f"{self.project_directory}/data/{file_data['friendly_name']}.csv", index=True)

        # Make Plot
        plt.figure(figsize=(12, 6))
        plt.plot(df_60th.index, df_60th['Light'], label='Light')
        plt.plot(df_60th.index, df_60th['Occupancy'], label='Occupancy')
        plt.xlabel('Timestamp')
        plt.ylabel('Value')
        plt.title(f"Light and Occupancy over time for {file_data['friendly_name']}")
        plt.legend()
        
        # Save the figure
        plt.savefig(f"{self.project_directory}/graphs/{file_data['friendly_name']}.png")

        # Add figure filepath to dir
        file_data['graph filepath'] = f"graphs/{file_data['friendly_name']}.png"
        
        
        # Add file to site
        self.site_data.update({friendly_name : file_data})
        with open(f'{self.project_directory}/sitedata.json', 'w') as json_file:
            json.dump(self.site_data, json_file, indent=4)
        print("Successful Import")

        self.load_json()
        self.clear_form()
        self.file_label = tk.Label(self, text=" ")
        self.file_label.grid(row = 6, column = 1, sticky = "w")

    
    def export_data(self):
        def validate_date(date_str):
            """Validate date string in the format YYYY-MM-DD HH:MM:SS."""
            try:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None

        #Get Start Time
        root = tk.Tk()
        root.withdraw()  # hide main window

        start_time = None
        while start_time is None:
            # Use a simpledialog to get the date
            date_str = simpledialog.askstring("Input", "Enter the start date/time in 'YYYY-MM-DD HH:MM:SS' format",
                                            parent=root)

            # Check if user clicked 'Cancel' or closed the dialog
            if date_str is None:
                print('No date was entered')
                return None, None

            start_time = validate_date(date_str)

            if start_time is None:
                tk.messagebox.showerror("Invalid input", "Please enter a valid date/time in 'YYYY-MM-DD HH:MM:SS' format")

        # Calculate the end time by adding one week
        end_time = start_time + timedelta(weeks=1)


        # Close the Tkinter root window
        root.destroy()