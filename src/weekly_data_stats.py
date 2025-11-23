import customtkinter as ctk
import tkinter
from tkinter import messagebox
import matplotlib

class weekly_stats:

    def __init__(self, parent, weather_json):

        self.weather_json = weather_json
        
        self.weekly_stats_window = ctk.CTkToplevel(parent)
        self.weekly_stats_window.title("Statistics Window")
        self.weekly_stats_window.geometry('1920x1080')

        print(weather_json)