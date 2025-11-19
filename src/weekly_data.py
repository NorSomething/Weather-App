import customtkinter as ctk
import tkinter
from tkinter import messagebox

class weekly_data:
    def __init__(self, parent, callback):

        self.callback = callback

        self.weekly_data_window = ctk.CTkToplevel(parent)
        self.weekly_data_window.title("Weekly Data")
        self.weekly_data_window.geometry('800x600')

        week = self.extract_weekly_data() #get weekly data

        self.label_heading = ctk.CTkLabel(self.weekly_data_window, text="This week's forecast.")
        self.label_heading.pack(padx = 20, pady = 20)

        self.label_min_temp = ctk.CTkLabel(self.weekly_data_window, text="")
        self.label_min_temp.pack(padx = 20, pady=20)
    
    def extract_weekly_data(self):
        return self.callback["days"][:7]
        #first seven days from main.py

