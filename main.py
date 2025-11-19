import requests
import tkinter
import customtkinter as ctk
import tkintermapview
import os
import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from dotenv import load_dotenv
import json

import world_map
import fav_place
import weekly_data

load_dotenv()

class Weather_GUI:

    def __init__(self):

        self.API_KEY = os.getenv('API_KEY')
        
        self.place = None #idk why I put it here, doesnt work without it
        self.fav_place = None

        self.root = ctk.CTk()

        self.root.geometry('1600x400')
        self.root.title('WeatherApp')

        self.info_window = None #for not creating extra windows

        self.date = datetime.datetime.now()
        self.current_date = str(self.date)[8:10] #might be useful when weekly data implementation

        self.user_selected_fav_loc = 0

        #Top Frame --> Title, Open Map Button, Show Information Button
        #Week Frame --> Days of the week
        #Info Frame --> Grid : each cell has one information
            #->> Basic Infos ->> Grid 
            #->> Description ->> not Grid
        #Conditional Frames --> Grid: each cell has information of stuff that needs computing (need sunscreen umrella)

        self.top_frame = ctk.CTkFrame(self.root, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.top_frame.pack(padx=20, pady=20, fill = 'x')

        self.top_frame.grid_columnconfigure((0), weight=1)
        self.top_frame.grid_rowconfigure((0), weight=1)
        
        self.fav_loc_frame = ctk.CTkFrame(self.root)
        self.fav_loc_frame.pack(padx=20, pady=20, fill = 'x') 

        self.fav_loc_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.fav_loc_frame.grid_rowconfigure((0,1,2,3), weight=1)

        #self.week_frame = ctk.CTkFrame(self.root, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        #self.week_frame.pack(padx=20, pady=20, fill = 'x')

        
        self.label = ctk.CTkLabel(self.top_frame, text='Weather App', font=('Arial', 55))
        self.label.grid(row = 0, column = 0, padx=10, pady=10)

        self.check_state = ctk.IntVar()

        self.button_map = ctk.CTkButton(self.top_frame, text='Open Map', command=self.show_map, font=('Arial', 30))
        self.button_map.grid(row = 1, column=0, padx=20, pady=20)

        self.button_get_fav1 = ctk.CTkButton(self.fav_loc_frame, text='Get Info of Fav Loc 1', command= lambda : self.return_favinfo('fav_place1'), font=('Arial', 30))
        self.button_get_fav1.grid(row = 2, column = 0, padx=20, pady=20)

        self.button_get_fav2 = ctk.CTkButton(self.fav_loc_frame, text='Get Info of Fav Loc 2', command= lambda : self.return_favinfo('fav_place2'), font=('Arial', 30))
        self.button_get_fav2.grid(row = 2, column = 1, padx=20, pady=20)

        self.button_get_fav3 = ctk.CTkButton(self.fav_loc_frame, text='Get Info of Fav Loc 3', command= lambda : self.return_favinfo('fav_place3'), font=('Arial', 30))
        self.button_get_fav3.grid(row = 2, column = 2, padx=20, pady=20)

        self.button_get_fav4 = ctk.CTkButton(self.fav_loc_frame, text='Get Info of Fav Loc 4', command= lambda : self.return_favinfo('fav_place4'), font=('Arial', 30))
        self.button_get_fav4.grid(row = 2, column = 3, padx=20, pady=20)

        self.root.mainloop()

    def show_map(self):
        world_map.world_map(self.root, self.return_coords)

    def return_coords(self,coords):
        print("return coords triggered", coords)
        self.place = coords
        self.user_selected_fav_loc = False
        self.display_info_window()

    def return_favinfo(self, loc_key):

        with open('fav_places.json', 'r') as f:
            data = json.load(f)

        cors = data[loc_key] 
            
        lat, long = cors[0], cors[1]

        self.user_selected_fav_loc = True

        self.fav_place = (lat, long)
        self.display_info_window()

    def umbrella_check(self, preprob):
        msg = "Umbrella is not needed today."
        if preprob >= 45:
            msg = "An Umbrella Would Come in Handy Today."
            return msg
        return msg
    
    def sunscreen_check(self, uvindex):
        msg = "Sunscreen is not needed today."
        if uvindex >= 3:
            msg = "Wear Sunscreen Before Going Out Today."
            return msg
        return msg


    def get_weather_data(self, coor):
        lat = coor[0]
        lon = coor[1]

        #visual crossing api -> with weekly stuff
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}?unitGroup=metric&key={self.API_KEY}"

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            messagebox.showerror("No Data", "Something went wrong with API\nPlease try again in a few minutes.")
    


    def display_info_window(self):

        if self.info_window is not None and self.info_window.winfo_exists():
            self.get_info()
            return 
        
        self.info_window = ctk.CTkToplevel(self.root)
        self.info_window.title("Info Window")
        self.info_window.geometry("1460x355")

        self.info_frame = ctk.CTkFrame(self.info_window)
        self.info_frame.pack(padx=20, pady=20, fill = 'x')

        self.basic_info_frame = ctk.CTkFrame(self.info_frame, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.basic_info_frame.pack(padx=20, pady=20, fill = 'x')

        self.basic_info_frame.grid_columnconfigure((0,1), weight=1)
        self.basic_info_frame.grid_rowconfigure((0,1,2), weight=1)

        self.desc_frame = ctk.CTkFrame(self.info_frame)
        self.desc_frame.pack(padx=20, pady=20, fill='x')

        self.desc_frame.grid_columnconfigure(0, weight=1)
        self.desc_frame.grid_rowconfigure(0, weight=1)

        self.conditional_frame = ctk.CTkFrame(self.root)
        self.conditional_frame.pack(padx=20, pady=20, fill = 'x')

        self.conditional_frame.grid_columnconfigure(0, weight=1)
        self.conditional_frame.grid_rowconfigure((0,1), weight=1)

        self.label_umbrella_check = ctk.CTkLabel(self.conditional_frame, text="")
        self.label_umbrella_check.grid(row=0, column=0, padx=10, pady=10)

        self.label_sunscreen_check = ctk.CTkLabel(self.conditional_frame, text="")
        self.label_sunscreen_check.grid(row=1, column= 0, padx=10, pady=10)


        self.label_current_dets_heading = ctk.CTkLabel(self.info_frame, text="")
        self.label_current_dets_heading.pack(padx=10,pady=10)

        self.label_current_temp = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_current_temp.grid(row = 0, column = 0, padx=10, pady=10, sticky='w')

        self.label_current_humidity = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_current_humidity.grid(row = 0, column = 1, padx=10, pady=10, sticky='w')

        self.label_current_description = ctk.CTkLabel(self.desc_frame, text="")
        self.label_current_description.grid(row = 0, column = 0, padx = 20, pady = 10)

        self.label_precip_percent = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_precip_percent.grid(row = 2, column = 0, padx=10, pady=10, sticky='w')

        self.labeL_uv_index = ctk.CTkLabel(self.basic_info_frame, text="")
        self.labeL_uv_index.grid(row = 2, column = 1, padx=10, pady=10, sticky='w')

        self.label_umbrella_check = ctk.CTkLabel(self.conditional_frame, text="")
        self.label_umbrella_check.grid(row=0, column=0, padx=10, pady=10)

        self.label_sunscreen_check = ctk.CTkLabel(self.conditional_frame, text="")
        self.label_sunscreen_check.grid(row=1, column= 0, padx=10, pady=10)


        self.get_info()
        
        
    def get_info(self):

        print("get info() triggered", self.place)
        print("date time is ", self.date)
        
        if self.user_selected_fav_loc:
            self.weather_info = self.get_weather_data(self.fav_place)
        else:
            self.weather_info = self.get_weather_data(self.place)

        if not self.weather_info:
            messagebox.showerror("Error", "No Data Found.")
            return

        #for weekly stuff:
        self.week = weekly_data.extract_weekly_data(self.weather_info) #calls the func in weekly_data.py
        print(self.week)

            
        current_temp = self.weather_info['currentConditions']["temp"]

        current_humidity = self.weather_info['currentConditions']['humidity']

        current_description = self.weather_info['description']

        current_uv_index = self.weather_info['currentConditions']['uvindex']

        current_precp_percent = self.weather_info['currentConditions']['precipprob']

        self.label_current_dets_heading.configure(text="Weather Information ", font=('Arial', 40))

        self.label_current_temp.configure(text=f"Current Temperature is : {current_temp:.2f} C.", font=('Arial', 30))
        self.label_current_humidity.configure(text=f"Current Humidity is : {current_humidity} percent.", font=('Arial', 30))
        self.label_current_description.configure(text=current_description, font=('Arial', 30))
        self.label_precip_percent.configure(text=f"Current Chance of Rain is : {current_precp_percent} percent.", font=('Arial', 30))
        self.labeL_uv_index.configure(text=f"Current UV Index is : {current_uv_index}.", font=('Arial', 30))
        self.label_umbrella_check.configure(text=self.umbrella_check(current_precp_percent), font=('Arial', 30))
        self.label_sunscreen_check.configure(text=self.sunscreen_check(current_uv_index), font=('Arial', 30))



Weather_GUI()


    





