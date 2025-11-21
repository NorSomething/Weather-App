import customtkinter as ctk
import tkinter
from tkinter import messagebox

class weekly_data:

    #note : fav places weekly temp does not update!!

    def __init__(self, parent, weekly_data_json):

        self.weekly_data_json = weekly_data_json

        self.weekly_data_window = ctk.CTkToplevel(parent)
        self.weekly_data_window.title("Weekly Data")
        self.weekly_data_window.geometry('1920x1080')

        week = self.extract_weekly_data() #get weekly data

        self.weekly_heading_frame = ctk.CTkFrame(self.weekly_data_window)
        self.weekly_heading_frame.pack(padx=20, pady=20)

        self.weekly_heading_frame.rowconfigure((0), weight=1)
        self.weekly_heading_frame.columnconfigure(0, weight=1)

        self.weekly_data_frame = ctk.CTkFrame(self.weekly_data_window)
        self.weekly_data_frame.pack(padx=20, pady=20)

        self.weekly_data_frame.rowconfigure((0), weight=1)
        self.weekly_data_frame.columnconfigure((0,1,2,3,4,5,6), weight=1)

        self.label_weekly_heading = ctk.CTkLabel(self.weekly_heading_frame, text="Weather for the next seven days", font=('Arial', 45))
        self.label_weekly_heading.grid(row=0, column=0, padx=20, pady=20)

        
        

        for i in range(7):

            day_date = week[i].get('datetime')

            min_temp = week[i].get('tempmin')
            max_temp = week[i].get('tempmax')
            humidity = week[i].get('humidity')
            precip = week[i].get('precip')
            condition = week[i].get('conditions')
            description = week[i].get('description')

            self.label_day_date = ctk.CTkLabel(self.weekly_data_frame, text=day_date, font=('Arial', 30))
            self.label_day_date.grid(row = 0, column = i, padx=20, pady=20)

            self.label_min_temp = ctk.CTkLabel(self.weekly_data_frame, text=min_temp, font=('Arial', 30))
            self.label_min_temp.grid(row = 1, column = i, padx = 20, pady = 20)

            self.label_max_temp = ctk.CTkLabel(self.weekly_data_frame, text=max_temp, font=('Arial', 30))
            self.label_max_temp.grid(row = 2, column = i, padx=20, pady=20)

            self.label_humidity = ctk.CTkLabel(self.weekly_data_frame, text=humidity, font=('Arial', 30))
            self.label_humidity.grid(row = 3, column = i, padx=20, pady=20)

            self.label_precip = ctk.CTkLabel(self.weekly_data_frame, text=precip, font=('Arial', 30))
            self.label_precip.grid(row = 4, column = i, padx=20, pady=20)

            self.label_condition = ctk.CTkLabel(self.weekly_data_frame, text=condition, wraplength=200, justify='center', font=('Arial', 30))
            self.label_condition.grid(row = 5, column = i, padx=20, pady=20)

            self.label_desc = ctk.CTkLabel(self.weekly_data_frame, text=description, wraplength=200, justify='center', font=('Arial', 30))
            self.label_desc.grid(row = 6, column = i, padx=20, pady=20)
        
    
    def extract_weekly_data(self):
        return self.weekly_data_json["days"][:7] #this is a list??
        #first seven days from main.py

