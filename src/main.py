import requests
import tkinter
import customtkinter as ctk
import tkintermapview
import os
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from dotenv import load_dotenv
import json
import threading
from geopy.geocoders import Nominatim
import time

import world_map
import fav_place
import weekly_data

load_dotenv()

#NOte : background colors super ugly as of now!! fix!!

class Weather_GUI:

    def __init__(self):

        self.API_KEY = os.getenv('API_KEY')
        
        self.place = None 
        self.fav_place = None
        self.week = None

        self.root = ctk.CTk()

        self.root.geometry('1200x840')
        self.root.title('WeatherApp')

        self.root.configure(fg_color='#101010')

        self.info_window = None #for not creating extra windows

        #self.date = datetime.datetime.now()

        self.user_selected_fav_loc = 0

        self.city_entered_check = False

        #Top Frame --> Title, Open Map Button, Show Information Button
        #Week Frame --> Days of the week
        #Info Frame --> Grid : each cell has one information
            #->> Basic Infos ->> Grid 
            #->> Description ->> not Grid
        #Conditional Frames --> Grid: each cell has information of stuff that needs computing (need sunscreen umrella)

        self.top_frame = ctk.CTkFrame(self.root, fg_color="#101010", border_width=6, border_color="#3A78C2", corner_radius=75)
        self.top_frame.pack(padx=20, pady=20)

        self.top_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.top_frame.grid_rowconfigure((0), weight=1)

        self.main_menu_frame = ctk.CTkFrame(self.root, fg_color='#101010', border_width=6, border_color="#3A78C2", corner_radius=75)
        self.main_menu_frame.pack(padx=20, pady=20)
        
        self.main_menu_frame.grid_columnconfigure((0,1), weight=1)
        self.main_menu_frame.grid_rowconfigure(0, weight=1)

        self.misc_buttons_frame = ctk.CTkFrame(self.main_menu_frame, fg_color='#101010', border_width=6, border_color="#3A78C2", corner_radius=50)
        self.misc_buttons_frame.grid(row = 0, column = 0, padx=20, pady=20)

        self.misc_buttons_frame.grid_columnconfigure(0, weight=1)
        self.misc_buttons_frame.grid_rowconfigure((0,1,2), weight=1)

        self.fav_loc_frame = ctk.CTkFrame(self.main_menu_frame, corner_radius=50, border_width=6, fg_color='#101010', border_color="#3A78C2")
        self.fav_loc_frame.grid(row = 0, column = 1, padx=20, pady=20) 

        self.fav_loc_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.fav_loc_frame.grid_rowconfigure((0,1,2,3), weight=1)
        
        self.label = ctk.CTkLabel(self.top_frame, text='Weather App', font=('Arial', 55))
        self.label.grid(row = 0, column=0,padx=10, pady=10)

        self.button_map = ctk.CTkButton(self.top_frame, text='Open Map', command=self.show_map, font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.button_map.grid(row = 1, column=0, padx=20, pady=20)

        self.text_box_city = ctk.CTkTextbox(self.top_frame, height=10, width=900, font=('Arial', 30))
        self.text_box_city.grid(row=2, column = 0, padx=20, pady=20)

        self.buttonn_get_city_info = ctk.CTkButton(self.top_frame, text="Get Weather Info of City : ", command=self.city_button_clicked, font=('Arial', 30) ,fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.buttonn_get_city_info.grid(row=3, column=0, padx=20, pady=20)

        #for fav places:
        self.geolocator = Nominatim(user_agent="my_geopy_app") #api intialisation

        with open('fav_places.json', 'r') as f:
            data = json.load(f)

        onel1, onel2 = data['fav_place1'][0], data['fav_place1'][1]
        twol1, twol2 = data['fav_place2'][0], data['fav_place2'][1]
        threel1, threel2 = data['fav_place3'][0], data['fav_place3'][1]
        fourl1, fourl2 = data['fav_place4'][0], data['fav_place4'][1]

        
        

        self.button_get_fav1 = ctk.CTkButton(self.fav_loc_frame, text=f'Get Info of Fav Loc : {self.get_loc_from_lat_long(onel1, onel2)}', command= lambda : self.return_favinfo('fav_place1'), font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.button_get_fav1.grid(row = 0, column = 0, padx=20, pady=20)

        self.button_get_fav2 = ctk.CTkButton(self.fav_loc_frame, text=f'Get Info of Fav Loc {self.get_loc_from_lat_long(twol1, twol2)}', command= lambda : self.return_favinfo('fav_place2'), font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white" )
        self.button_get_fav2.grid(row = 1, column = 0, padx=20, pady=20)

        self.button_get_fav3 = ctk.CTkButton(self.fav_loc_frame, text=f'Get Info of Fav Loc {self.get_loc_from_lat_long(threel1, threel2)}', command= lambda : self.return_favinfo('fav_place3'), font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.button_get_fav3.grid(row = 2, column = 0, padx=20, pady=20)

        self.button_get_fav4 = ctk.CTkButton(self.fav_loc_frame, text=f'Get Info of Fav Loc {self.get_loc_from_lat_long(fourl1, fourl2)}', command= lambda : self.return_favinfo('fav_place4'), font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.button_get_fav4.grid(row = 3, column = 0, padx=20, pady=20)

        self.button_get_weekly = ctk.CTkButton(self.misc_buttons_frame, text="Get Weekly Info", command= self.get_weekly_info,  font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.button_get_weekly.grid(row = 0, column = 0, padx=20, pady=20)

        self.button_refresh_window = ctk.CTkButton(self.misc_buttons_frame, text="Refresh Window", command=self.create_refresh_thread, fg_color="#4A90E2", hover_color="#3A78C2", text_color="white", font=('Arial', 30))
        self.button_refresh_window.grid(row = 1, column = 0, padx=20, pady=20)

        self.label_current_selected_location = ctk.CTkLabel(self.misc_buttons_frame, text="No Location Selected", font=('Arial', 30))
        self.label_current_selected_location.grid(row = 2, column = 0, padx = 20, pady=20)

        # self.set_all_themes()

        self.root.mainloop()

    def create_refresh_thread(self):
        self.show_refresh_loading()

        threading.Thread(target=self.refresh_windows, daemon=True).start()

    def refresh_windows(self):
        

        with open('fav_places.json', 'r') as f:
            data = json.load(f)


        onel1, onel2 = data['fav_place1']
        twol1, twol2 = data['fav_place2']
        threel1, threel2 = data['fav_place3']
        fourl1, fourl2 = data['fav_place4']

        self.button_get_fav1.configure(text=f'Get Info of Fav Loc : {self.get_loc_from_lat_long(onel1, onel2)}')
        self.button_get_fav2.configure(text=f'Get Info of Fav Loc : {self.get_loc_from_lat_long(twol1, twol2)}')
        self.button_get_fav3.configure(text=f'Get Info of Fav Loc : {self.get_loc_from_lat_long(threel1, threel2)}')
        self.button_get_fav4.configure(text=f'Get Info of Fav Loc : {self.get_loc_from_lat_long(fourl1, fourl2)}')

        #current loc refresh
        if self.place is None:
            self.label_current_selected_location.configure(text="No Location Selected")
        else:
            loc = self.get_loc_from_lat_long(self.place[0], self.place[1])
            self.label_current_selected_location.configure(text=f"Current Selected Location : {loc}")

        self.hide_refresh_loading()


    def get_loc_from_lat_long(self, Latitude, Longitude):
        location = self.geolocator.reverse(str(Latitude)+","+str(Longitude))
        address = location.raw['address']
        
        return address.get('city', '')
        

    def show_loading(self):
        self.loading_bar = ctk.CTkProgressBar(self.info_window, mode='indeterminant')
        self.loading_bar.pack(padx=10, pady=10)
        self.loading_bar.start()

    def hide_loading(self):
        if hasattr(self, 'loading_bar'): #if bar is still on screen
            self.loading_bar.stop()
            self.loading_bar.destroy()

    def show_refresh_loading(self):
        self.refresh_loading = ctk.CTkProgressBar(self.root, mode='indeterminate')
        self.refresh_loading.pack(pady=10)
        self.refresh_loading.start()

    def hide_refresh_loading(self):
        if hasattr(self, 'refresh_loading'):
            self.refresh_loading.stop()
            self.refresh_loading.destroy()

    def show_weekly_loading(self):
        self.weekly_loading = ctk.CTkProgressBar(self.root, mode='indeterminate')
        self.weekly_loading.pack(pady=10)
        self.weekly_loading.start()

    def hide_weekly_loading(self):
        if hasattr(self, 'weekly_loading'):
            self.weekly_loading.stop()
            self.weekly_loading.destroy()

    def show_moon_phases(self, moon_phase):

        image_directory = os.path.join(os.path.dirname(__file__), "moon_phase_bin") #__file__ is current working directory
        #image_directory holds image paths

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

        self.root.__img_ref = tk_img

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
        if preprob is None:
            return "Rain Probability Not Available."
        msg = "Umbrella is not needed today."
        if preprob >= 45:
            msg = "An Umbrella Would Come in Handy Today."
            return msg
        return msg
    
    def sunscreen_check(self, uvindex):
        if uvindex is None:
            return "UV Index Not Available"
        msg = "Sunscreen is not needed today."
        if uvindex >= 3:
            msg = "Wear Sunscreen Before Going Out Today."
            return msg
        return msg

    '''
    main.py fetches JSON
    main.py passes JSON into weekly_data
    weekly_data extracts first 7 days
    weekly window displays them'''

    def get_weekly_info(self):

        if self.place is None and not self.user_selected_fav_loc:
            messagebox.showwarning("No Location", "Select a location first.")
            return
        
        #week_weather is the whole dict 

        self.show_weekly_loading()
        threading.Thread(target=self.fetch_weekly_thread, daemon=True).start() #if user closes while loading, the loading will take place in backgroud, to avoid that daemon?

    def fetch_weekly_thread(self):
        
        if self.user_selected_fav_loc:
            week_weather = self.get_weather_data(self.fav_place)
        else:
            week_weather = self.get_weather_data(self.place)

        #update gui
        self.root.after(0, lambda: self.open_weekly_window(week_weather))

    def open_weekly_window(self, week_weather):
        self.hide_weekly_loading()
        weekly_data.weekly_data(self.root, week_weather) #calls the weekly window from weekly_data.py


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
    
    def get_weather_data_city(self, city):

        #self.city_entered_check = True

        #visual crossing api -> with weekly stuff
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={self.API_KEY}"

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            messagebox.showerror("No Data", "Something went wrong with API\nPlease try again in a few minutes.")

    def city_button_clicked(self):
        
        city = self.text_box_city.get("1.0", "end").strip().lower()

        if city == "":
            messagebox.showwarning("Empty City", "Please enter a city name.")
            return

        self.city_entered_check = True
        self.user_selected_fav_loc = False
        
        location = self.geolocator.geocode(city)
        coords = (location.latitude, location.longitude)

        if coords == None:
            messagebox.showerror("Error", "City not found, Try again.")

        self.place = coords

        
        self.display_info_window()

    def make_box(self, parent, text="", font=('Arial', 30)):
        box = ctk.CTkFrame(parent, fg_color="#101010", border_width=6, border_color="#4da6ff",corner_radius=75, width=280, height=90)
        box.pack_propagate(False)

        label = ctk.CTkLabel(box, text=text, font=font, anchor="center", wraplength=260)
        label.pack(expand=True, padx=10, pady=10)

        return box, label


    def display_info_window(self):

        if self.info_window is not None and self.info_window.winfo_exists():
            self.get_info()
            return

        self.info_window = ctk.CTkToplevel(self.root)
        self.info_window.title("Info Window")
        self.info_window.geometry("1000x1000")
        self.info_window.configure(fg_color='#101010')

        self.info_frame = ctk.CTkFrame(self.info_window, fg_color="#101010")
        self.info_frame.pack(pady=20)

        self.label_heading = ctk.CTkLabel(self.info_frame, text="Information Window", font=("Helvetica", 40))
        self.label_heading.pack(pady=20)

        basic_grid = ctk.CTkFrame(self.info_frame, fg_color="#101010")
        basic_grid.pack(pady=10)

        self.temp_box, self.label_current_temp = self.make_box(basic_grid)
        self.temp_box.grid(row=0, column=0, padx=20, pady=10)

        self.humidity_box, self.label_current_humidity = self.make_box(basic_grid)
        self.humidity_box.grid(row=0, column=1, padx=20, pady=10)

        self.precip_box, self.label_precip_percent = self.make_box(basic_grid)
        self.precip_box.grid(row=1, column=0, padx=20, pady=10)

        self.uv_box, self.labeL_uv_index = self.make_box(basic_grid)
        self.uv_box.grid(row=1, column=1, padx=20, pady=10)

        self.sunrise_box, self.label_sunrise_time = self.make_box(basic_grid)
        self.sunrise_box.grid(row=2, column=0, padx=20, pady=10)

        self.sunset_box, self.label_sunset_time = self.make_box(basic_grid)
        self.sunset_box.grid(row=2, column=1, padx=20, pady=10)

        self.desc_box, self.label_current_description = self.make_box(self.info_frame, font=("Arial", 24))
        self.desc_box.configure(width=600, height=120)
        self.desc_box.pack(pady=15)

        cond_grid = ctk.CTkFrame(self.info_frame, fg_color="#101010")
        cond_grid.pack(pady=10)

        self.umbrella_box, self.label_umbrella_check = self.make_box(cond_grid)
        self.umbrella_box.grid(row=0, column=0, padx=20, pady=10)

        self.sunscreen_box, self.label_sunscreen_check = self.make_box(cond_grid)
        self.sunscreen_box.grid(row=0, column=1, padx=20, pady=10)

        self.moon_box = ctk.CTkFrame(self.info_frame,fg_color="#262626",border_width=2, border_color="#4da6ff", corner_radius=15,width=180, height=180)
        self.moon_box.pack(pady=20)

        self.label_current_moon_phase = ctk.CTkLabel(self.moon_box, image=None, text="")
        self.label_current_moon_phase.pack(expand=True, padx=10, pady=10)

        #loading bar
        self.show_loading()
        threading.Thread(target=self.load_weather_thread_info_window, daemon=True).start()


    def load_weather_thread_info_window(self):
        self.get_info()
        self.info_window.after(0, self.hide_loading) #just self.hide_loading() is unsafe => called inside background thread
        


    def get_info(self):

        print("get info() triggered", self.place)

            
        if self.city_entered_check:
            city = self.text_box_city.get("1.0", "end").strip().lower()
            self.weather_info = self.get_weather_data_city(city)
            self.city_entered_check = False

        elif self.user_selected_fav_loc:
            self.weather_info = self.get_weather_data(self.fav_place)
        
        else:
            self.weather_info = self.get_weather_data(self.place)

        if not self.weather_info:
            messagebox.showerror("Error", "No Data Found.")
            return

            
        current_temp = self.weather_info['currentConditions']["temp"]

        current_humidity = self.weather_info['currentConditions']['humidity']

        current_description = self.weather_info['description']
        
        current_uv_index = self.weather_info['currentConditions']['uvindex']

        current_precip_percent = self.weather_info['currentConditions']['precipprob']

        sunrise_time = self.weather_info['days'][0].get("sunrise", 0)
        sunset_time = self.weather_info['days'][0].get("sunset", 0)

        currnet_moon_phase = self.weather_info['currentConditions']['moonphase']

        moon_image = self.show_moon_phases(currnet_moon_phase) #moon phase still needs more details

        current_time = self.weather_info['currentConditions']['datetime']

        self.label_current_description.configure(text="Weather Information ", font=('Arial', 40))

        self.label_current_temp.configure(text=f"Current Temperature is : {current_temp:.1f}°C.", font=('Arial', 25))
        self.label_current_humidity.configure(text=f"Current Humidity is : {current_humidity} percent.", font=('Arial', 25))
        self.label_current_description.configure(text=current_description, font=('Arial', 25))
        self.label_precip_percent.configure(text=f"Current Chance of Rain is : {current_precip_percent} percent.", font=('Arial', 25))
        self.labeL_uv_index.configure(text=f"Current UV Index is : {current_uv_index}.", font=('Arial', 25))
        self.label_umbrella_check.configure(text=self.umbrella_check(current_precip_percent), font=('Arial', 25))
        self.label_sunscreen_check.configure(text=self.sunscreen_check(current_uv_index), font=('Arial', 25))
        self.label_sunrise_time.configure(text=f"Sunrise Time : {sunrise_time}", font=('Arial', 25))
        self.label_sunset_time.configure(text=f"Sunset Time : {sunset_time}", font=('Arial', 25))
        self.label_current_moon_phase.configure(image = moon_image, text="")



if __name__ == '__main__':
    Weather_GUI()