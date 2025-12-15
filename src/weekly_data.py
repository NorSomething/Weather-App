import customtkinter as ctk
import tkinter
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import matplotlib 
import numpy as np

import weekly_data_stats
from main import Weather_GUI

class weekly_data:


    def __init__(self, parent, weekly_data_json):

        self.weekly_data_json = weekly_data_json

        self.weekly_data_window = ctk.CTkToplevel(parent)
        self.weekly_data_window.title("Weekly Data")
        self.weekly_data_window.geometry('1920x1080')

        self.weekly_data_window.configure(fg_color='#101010')

        week = self.extract_weekly_data() #get weekly data

        self.weekly_heading_frame = ctk.CTkFrame(self.weekly_data_window, fg_color='#101010', border_width=6, border_color="#3A78C2", corner_radius=75)
        self.weekly_heading_frame.pack(padx=20, pady=20)

        self.weekly_heading_frame.rowconfigure((0), weight=1)
        self.weekly_heading_frame.columnconfigure(0, weight=1)

        self.weekly_data_frame = ctk.CTkFrame(self.weekly_data_window, fg_color='#101010', border_width=6, border_color="#3A78C2", corner_radius=75)
        self.weekly_data_frame.pack(padx=10, pady=10)

        self.weekly_data_frame.rowconfigure((0), weight=1)
        self.weekly_data_frame.columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        self.label_weekly_heading = ctk.CTkLabel(self.weekly_heading_frame, text="Weather for the next seven days", font=('Arial', 45))
        self.label_weekly_heading.grid(row=0, column=0, padx=20, pady=20)

        self.button_get_weekly_graphs = ctk.CTkButton(self.weekly_heading_frame, text="Get Statistical Data", command=self.open_weeky_stats_window, fg_color="#4A90E2", hover_color="#3A78C2", text_color="white", font=('Arial', 30))
        self.button_get_weekly_graphs.grid(row=1, column=0, padx=20, pady=20)
        
        self.days = []
        self.min_temp_array = []
        self.max_temp_array = []
        self.humidity_array = []
        self.precip_array = []
        self.sunrise_array = []
        self.sunset_array = []


        for i in range(8):

            day_date = week[i+1].get('datetime')

            min_temp = week[i+1].get('tempmin')
            max_temp = week[i+1].get('tempmax')
            humidity = week[i+1].get('humidity')
            precip = week[i+1].get('precip')
            condition = week[i+1].get('conditions')
            description = week[i+1].get('description')
            sunrise = week[i+1].get('sunrise')
            sunset = week[i+1].get('sunset')
            moonphase = week[i+1].get('moonphase')

            self.days.append(day_date)
            self.min_temp_array.append(min_temp)
            self.max_temp_array.append(max_temp)
            self.humidity_array.append(humidity)
            self.precip_array.append(precip)
            self.sunrise_array.append(sunrise)
            self.sunset_array.append(sunset)
            

            self.label_label_mintemp = ctk.CTkLabel(self.weekly_data_frame, text="Minimum Temperature", wraplength=200, justify='center',font=('Arial', 30))
            self.label_label_mintemp.grid(row = 1, column = 0, padx=10, pady=10)

            self.label_label_maxtemp = ctk.CTkLabel(self.weekly_data_frame, text="Maximum Temperature", wraplength=200, justify='center', font=('Arial', 30))
            self.label_label_maxtemp.grid(row = 2, column = 0, padx=10, pady=10)

            self.label_label_humidity = ctk.CTkLabel(self.weekly_data_frame, text="Humidity", wraplength=200, justify='center', font=('Arial', 30))
            self.label_label_humidity.grid(row = 3, column = 0, padx=10, pady=10)

            self.label_label_precip = ctk.CTkLabel(self.weekly_data_frame, text="Precipitation", wraplength=200, justify='center', font=('Arial', 30))
            self.label_label_precip.grid(row = 4, column = 0, padx=10, pady=10)

            self.label_label_sunrise = ctk.CTkLabel(self.weekly_data_frame, text="Sunrise", wraplength=200, justify='center', font=('Arial', 30))
            self.label_label_sunrise.grid(row = 5, column = 0, padx=10, pady=10)

            self.label_label_sunset = ctk.CTkLabel(self.weekly_data_frame, text="Sunset", wraplength=200, justify='center', font=('Arial', 30))
            self.label_label_sunset.grid(row = 6, column = 0, padx=10, pady=10)

            self.label_label_cond = ctk.CTkLabel(self.weekly_data_frame, text="Condition", wraplength=200, justify='center', font=('Arial', 30))
            self.label_label_cond.grid(row = 7, column = 0, padx=10, pady=10)

            self.label_label_moonphase = ctk.CTkLabel(self.weekly_data_frame, text="Moon Phases", wraplength=200, justify='center', font=('Arial', 30))
            self.label_label_moonphase.grid(row = 8, column = 0, padx=10, pady=10)

            self.label_day_date = ctk.CTkLabel(self.weekly_data_frame, text=day_date, font=('Arial', 30))
            self.label_day_date.grid(row = 0, column = i+1, padx=10, pady=10)

            self.label_min_temp = ctk.CTkLabel(self.weekly_data_frame, text=min_temp, font=('Arial', 30))
            self.label_min_temp.grid(row = 1, column = i+1, padx = 20, pady = 20)

            self.label_max_temp = ctk.CTkLabel(self.weekly_data_frame, text=max_temp, font=('Arial', 30))
            self.label_max_temp.grid(row = 2, column = i+1, padx=10, pady=10)

            self.label_humidity = ctk.CTkLabel(self.weekly_data_frame, text=humidity, font=('Arial', 30))
            self.label_humidity.grid(row = 3, column = i+1, padx=10, pady=10)

            self.label_precip = ctk.CTkLabel(self.weekly_data_frame, text=precip, font=('Arial', 30))
            self.label_precip.grid(row = 4, column = i+1, padx=10, pady=10)

            self.label_sunrise = ctk.CTkLabel(self.weekly_data_frame, text=sunrise, font=('Arial', 30))
            self.label_sunrise.grid(row = 5, column = i+1, padx=10, pady=10)

            self.label_sunset = ctk.CTkLabel(self.weekly_data_frame, text=sunset, font=('Arial', 30))
            self.label_sunset.grid(row = 6, column = i+1, padx=10, pady=10)

            self.label_condition = ctk.CTkLabel(self.weekly_data_frame, text=condition, wraplength=200, justify='center', font=('Arial', 30))
            self.label_condition.grid(row = 7, column = i+1, padx=10, pady=10)

            img = self.put_moon_phase(moonphase)

            self.label_moon_phase = ctk.CTkLabel(self.weekly_data_frame, text="", image=img, wraplength=200, justify='center')
            self.label_moon_phase.grid(row = 8, column = i+1, padx=10, pady=10)


    
    def put_moon_phase(self, moon_phase):
        image_directory = os.path.join(os.path.dirname(__file__), "moon_phase_bin")
        
        img = None

        if 0 <= moon_phase <= 0.24:
            img = Image.open(os.path.join(image_directory, "waxing_crescent.png"))
        elif moon_phase == 0.25:
            img = Image.open(os.path.join(image_directory, "first_quarter.png"))
        elif 0.26 <= moon_phase <= 0.49:
            img = Image.open(os.path.join(image_directory, "waxing_gibbous.png"))
        elif moon_phase == 0.5:
            img = Image.open(os.path.join(image_directory, "full_moon.png"))
        elif 0.51 <= moon_phase <= 0.74:
            img = Image.open(os.path.join(image_directory, "wanning_gibbous.png"))
        elif moon_phase == 0.75: 
            img = Image.open(os.path.join(image_directory, "third_quarter.png"))
        elif 0.76 <= moon_phase <= 0.99:
            img = Image.open(os.path.join(image_directory, "waning_crescent.png"))



        img = img.resize((150,150))
        tk_img = ImageTk.PhotoImage(img)

        return tk_img

    def extract_weekly_data(self):
        return self.weekly_data_json["days"][:8] 
        #first seven days from main.py

    def open_weeky_stats_window(self):
        data_list = []
        data_list.append(self.days)
        data_list.append(self.min_temp_array)
        data_list.append(self.max_temp_array)
        data_list.append(self.humidity_array)
        data_list.append(self.precip_array)
        data_list.append(self.sunrise_array)
        data_list.append(self.sunset_array)
        weekly_data_stats.weekly_stats(self.weekly_data_window,  data_list) 