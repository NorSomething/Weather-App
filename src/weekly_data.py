import customtkinter as ctk
import tkinter
from tkinter import messagebox

class weekly_data:
    def __init__(self, parent, weekly_data_json):

        self.weekly_data_json = weekly_data_json

        self.weekly_data_window = ctk.CTkToplevel(parent)
        self.weekly_data_window.title("Weekly Data")
        self.weekly_data_window.geometry('800x600')

        week = self.extract_weekly_data() #get weekly data

        self.weekly_heading_frame = ctk.CTkFrame(self.weekly_data_window)
        self.weekly_heading_frame.pack(padx=20, pady=20)

        self.weekly_heading_frame.rowconfigure((0), weight=1)
        self.weekly_heading_frame.columnconfigure(0, weight=1)

        self.weekly_data_frame = ctk.CTkFrame(self.weekly_data_window)
        self.weekly_data_frame.pack(padx=20, pady=20)

        self.weekly_data_frame.rowconfigure((0), weight=1)
        self.weekly_data_frame.columnconfigure(0, weight=1)

        self.label_weekly_heading = ctk.CTkLabel(self.weekly_heading_frame, text="This Week's Report", font=('Arial', 45))
        self.label_weekly_heading.grid(row=0, column=0, padx=20, pady=20)

        for i in range(7):
            self.label_weekly_heading = ctk.CTkLabel(self.weekly_data_frame, text="", font=("Arial", 30))
            self.label_weekly_heading.grid(row=0, column=i, padx=20, pady=20)
    
    def extract_weekly_data(self):
        return self.weekly_data_json["days"][:7]
        #first seven days from main.py

