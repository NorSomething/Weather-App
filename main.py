import requests
import tkinter
import customtkinter as ctk
import tkintermapview
import os
from tkinter import messagebox
from tkinter import PhotoImage
from dotenv import load_dotenv

load_dotenv()

class Weather_GUI:

    def __init__(self):

        self.API_KEY = os.getenv('API_KEY')
        
        self.place = None #idk why I put it here, doesnt work without it

        self.root = ctk.CTk()

        self.root.geometry('1600x1200')
        self.root.title('WeatherApp')


        self.label = ctk.CTkLabel(self.root, text='Weather App', font=('Arial', 55))
        self.label.pack(padx=10, pady=10)

        self.check_state = ctk.IntVar()

        self.button = ctk.CTkButton(self.root, text='Open Map', command=self.show_map, font=('Arial', 30))
        self.button.pack(padx=20, pady=20)

        self.button = ctk.CTkButton(self.root, text='Get Weather Information', command=self.get_info, font=('Arial', 30))
        self.button.pack(padx=20, pady=10)

        self.label_current_temp = ctk.CTkLabel(self.root, text="")
        self.label_current_temp.pack(padx=10, pady=10, anchor='w')

        self.label_current_humidity = ctk.CTkLabel(self.root, text="")
        self.label_current_humidity.pack(padx=10, pady=10, anchor='w')

        self.root.mainloop()

    def show_map(self):
        world_map(self.root, self.return_coords)

    def return_coords(self,coords):
        self.place = coords


    def get_weather_data(self, coor):
        lat = coor[0]
        lon = coor[1]

        #open weather map api
        # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}&units=metric"
        
        #open meteo api
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}?key={self.API_KEY}"

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            pass
        
    def get_info(self):
        
        self.weather_info = self.get_weather_data(self.place)
            
        current_temp = self.weather_info['currentConditions']["temp"]
        current_humidity = self.weather_info['currentConditions']['humidity']

        self.label_current_temp.configure(text=f"Current Temperature in ____ is : {current_temp} C.", font=('Arial', 30))
        self.label_current_humidity.configure(text=f"Current Humidity in ____is : {current_humidity} percent.", font=('Arial', 30))


class world_map:

    def __init__(self, parent, callback):
        
        self.callback = callback

        self.window = ctk.CTkToplevel(parent)
        self.window.geometry('800x600')

        map_widget = tkintermapview.TkinterMapView(self.window, width=800, height=600, corner_radius=0)
        map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        self.position = None
        map_widget.add_left_click_map_command(self.put_marker)

    def put_marker(self, coords):
        print(coords)
        self.callback(coords)
        

Weather_GUI()


    





