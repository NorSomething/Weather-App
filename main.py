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

        #Top Frame --> Title, Open Map Button, Show Information Button
        #Week Frame --> Days of the week
        #Info Frame --> Grid : each cell has one information
            #->> Basic Infos ->> Grid 
            #->> Description ->> not Grid

        self.top_frame = ctk.CTkFrame(self.root, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.top_frame.pack(padx=20, pady=20, fill = 'x')

        self.week_frame = ctk.CTkFrame(self.root, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.week_frame.pack(padx=20, pady=20, fill = 'x')

        self.info_frame = ctk.CTkFrame(self.root)
        self.info_frame.pack(padx=20, pady=20, fill = 'x')

        self.basic_info_frame = ctk.CTkFrame(self.info_frame, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.basic_info_frame.pack(padx=20, pady=20, fill = 'x')

        self.desc_frame = ctk.CTkFrame(self.info_frame)
        self.desc_frame.pack(padx=20, pady=20, fill='x')

        self.label = ctk.CTkLabel(self.top_frame, text='Weather App', font=('Arial', 55))
        self.label.pack(padx=10, pady=10)

        self.check_state = ctk.IntVar()

        self.button = ctk.CTkButton(self.top_frame, text='Open Map', command=self.show_map, font=('Arial', 30))
        self.button.pack(padx=20, pady=20)

        #self.day1_button = ctk.CTkButton(self.week_frame, text="Sunday", command=self.get_info, font=('Arial', 30))
        #self.day1_button.grid(row = 1, column = 0, padx=20, pady=20, sticky = 'w')

        self.label_current_temp = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_current_temp.grid(row = 0, column = 0, padx=10, pady=10, sticky='w')

        self.label_current_humidity = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_current_humidity.grid(row = 0, column = 1, padx=10, pady=10, sticky='w')

        self.label_current_description = ctk.CTkLabel(self.desc_frame, text="")
        self.label_current_description.grid(row = 2, column = 0, padx = 20, pady = 10, sticky='w')

        self.root.mainloop()

    def show_map(self):
        world_map(self.root, self.return_coords)

    def return_coords(self,coords):
        print("return coords triggered", coords)
        self.place = coords
        self.get_info()


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

        print("get info() triggered", self.place)
        
        self.weather_info = self.get_weather_data(self.place)
            
        current_temp = self.weather_info['currentConditions']["temp"]
        current_temp = (current_temp - 32)/1.8

        current_humidity = self.weather_info['currentConditions']['humidity']

        current_description = self.weather_info['description']

        self.label_current_temp.configure(text=f"Current Temperature in ____ is : {current_temp:.2f} C.", font=('Arial', 30))
        self.label_current_humidity.configure(text=f"Current Humidity in ____is : {current_humidity} percent.", font=('Arial', 30))
        self.label_current_description.configure(text=current_description, font=('Arial', 30))



class world_map:

    def __init__(self, parent, callback):

        self.callback = callback

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Map")
        self.window.geometry('800x600')

        self.weather_map_frame = ctk.CTkFrame(self.window)
        self.weather_map_frame.pack(side='bottom', fill='x', pady=5)

        self.map_widget = tkintermapview.TkinterMapView(self.window, width=800, height=600, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        self.position = None
        self.map_widget.add_left_click_map_command(self.put_marker)

        self.label_find_information_button = ctk.CTkButton(self.weather_map_frame, command=self.select_pos, text="Find Information")
        self.label_find_information_button.pack(padx = 10, pady = 10)

        self.label_instructions = ctk.CTkLabel(self.weather_map_frame, text='Click on the place and press the button below to find information.', font=('Arial',22))
        self.label_instructions.pack(padx=10, pady=10)


    def put_marker(self, coords):
        print("put marker() triggered", coords)
        self.map_widget.set_marker(coords[0], coords[1], text="Selected Location")
        self.position = coords
        #print(coords, "have been selected.")

    def select_pos(self):
        print("select pos() triggered", self.position)
        if self.position:
            self.callback(self.position)

        

Weather_GUI()


    





