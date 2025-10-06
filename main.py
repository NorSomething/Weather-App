import requests
import tkinter as tk
import customtkinter as ctk
import os
from tkinter import messagebox
from tkinter import PhotoImage
from dotenv import load_dotenv

load_dotenv()

class Weather_GUI:

    def __init__(self):

        self.API_KEY = os.getenv('API_KEY')
        
        self.root = ctk.CTk()

        self.root.geometry('800x600')
        self.root.title('WeatherApp')

        #city = input("Enter City : ")

        self.label = ctk.CTkLabel(self.root, text='Weather App', font=('Arial', 55))
        self.label.pack(padx=10, pady=10)

        self.textbox = ctk.CTkTextbox(self.root, height=10, font=('Arial', 45))
        self.textbox.pack(padx=10, pady=10)

        self.check_state = ctk.IntVar()

        self.button = ctk.CTkButton(self.root, text='Get Weather Information', command=self.get_info, font=('Arial', 30))
        self.button.pack(padx=20, pady=10)

        self.label_current_temp = ctk.CTkLabel(self.root, text="")
        self.label_current_temp.pack(padx=10, pady=10, anchor='w')

        self.root.mainloop()

    def get_weather_data(self, ci):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ci}&appid={self.API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            pass
        
    def get_info(self):
        self.city_name = self.textbox.get('1.0', 'end').strip().lower()
        self.weather_info = self.get_weather_data(self.city_name)
            
        current_temp = self.weather_info['main']["temp"]

        self.label_current_temp.configure(text=f"Current Temperature in {self.city_name.title()} is : {current_temp} C.", font=('Arial', 30))



        #weather_info = get_weather_data(city)

Weather_GUI()


    





