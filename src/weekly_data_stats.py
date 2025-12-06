import customtkinter as ctk
import tkinter
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

class weekly_stats:

    def __init__(self, parent, weather_json, data_list):

        self.weather_json = weather_json
        self.data_list = data_list
        
        self.weekly_stats_window = ctk.CTkToplevel(parent)
        self.weekly_stats_window.title("Statistics Window")
        self.weekly_stats_window.geometry('640x300')

        self.weekly_buttons_frame = ctk.CTkFrame(self.weekly_stats_window)
        self.weekly_buttons_frame.pack(padx = 20, pady=20, fill='x')

        self.weekly_buttons_frame.columnconfigure((0,1), weight=1)
        self.weekly_buttons_frame.rowconfigure((0,1,2), weight=1)

        self.dates = np.array(self.data_list[0])    
        self.min_temp = np.array(self.data_list[1])
        self.max_temp = np.array(self.data_list[2])
        self.humidity = np.array(self.data_list[3])
        self.precip = np.array(self.data_list[4])
        self.sunrise = np.array(self.data_list[5])
        self.sunset = np.array(self.data_list[6])

        self.button_min_temp_graph = ctk.CTkButton(self.weekly_buttons_frame, text="Get MinTemp Graph", command= lambda: self.get_graph(self.min_temp, "Minimum Temperate Variation in the following week.","Temperature in C"), font=('Arial', 30)) #lamba here as you cant give arg here
        self.button_min_temp_graph.grid(row = 0, column = 0, padx = 20, pady=20)

        self.button_max_temp = ctk.CTkButton(self.weekly_buttons_frame, text="Get MaxTemp Graph", command= lambda: self.get_graph(self.max_temp, "Maximum Temperate Variation in the following week.","Temperature in C"), font=('Arial', 30)) #lamba here as you cant give arg here
        self.button_max_temp.grid(row = 1, column = 0, padx = 20, pady=20)

        self.button_humidity = ctk.CTkButton(self.weekly_buttons_frame, text="Get Humidity Graph", command= lambda: self.get_graph(self.humidity, "Humidity Variation in the following week.","Preesure in mm of Hg"), font=('Arial', 30)) #lamba here as you cant give arg here
        self.button_humidity.grid(row = 2, column = 0, padx = 20, pady=20)

        self.button_precip = ctk.CTkButton(self.weekly_buttons_frame, text="Get Precip Graph", command= lambda: self.get_graph(self.precip, "Precipitation Variation in the following week.",""), font=('Arial', 30)) #lamba here as you cant give arg here
        self.button_precip.grid(row = 0, column = 1, padx = 20, pady=20)

        self.button_sunrise = ctk.CTkButton(self.weekly_buttons_frame, text="Get Sunrise Graph", command= lambda: self.get_graph(self.sunrise, "Sunrise Time Variation in the following week.",""), font=('Arial', 30)) #lamba here as you cant give arg here
        self.button_sunrise.grid(row = 1, column = 1, padx = 20, pady=20)

        self.button_precip = ctk.CTkButton(self.weekly_buttons_frame, text="Get Sunset Graph", command= lambda: self.get_graph(self.sunset, "Sunset Time Variation in the following week.",""), font=('Arial', 30)) #lamba here as you cant give arg here
        self.button_precip.grid(row = 2, column = 1, padx = 20, pady=20)
        

    def get_graph(self, ycoords, title, ylabel):

        width_px = 1280
        height_px = 720
        dpi = 100
        
        ypoints = np.array(ycoords)
        plt.figure(figsize=(width_px/dpi, height_px/dpi), dpi=dpi)
        plt.plot(self.dates, ypoints)

        plt.xlabel("Dates")
        plt.ylabel(ylabel)
        plt.title(title)

        plt.grid()
        plt.show()


        