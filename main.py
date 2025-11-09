import requests
import tkinter
import customtkinter as ctk
import tkintermapview
import os
import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from dotenv import load_dotenv

load_dotenv()

class Weather_GUI:

    def __init__(self):

        self.API_KEY = os.getenv('API_KEY')
        
        self.place = None #idk why I put it here, doesnt work without it
        self.fav_place = None

        self.root = ctk.CTk()

        self.root.geometry('1920x1080')
        self.root.title('WeatherApp')

        self.date = datetime.datetime.now()
        self.current_date = str(self.date)[8:10]

        self.user_selected_fav_loc = 0

        #Top Frame --> Title, Open Map Button, Show Information Button
        #Week Frame --> Days of the week
        #Info Frame --> Grid : each cell has one information
            #->> Basic Infos ->> Grid 
            #->> Description ->> not Grid
        #Conditional Frames --> Grid: each cell has information of stuff that needs computing (need sunscreen umrella)

        self.top_frame = ctk.CTkFrame(self.root, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.top_frame.pack(padx=20, pady=20, fill = 'x')

        self.week_frame = ctk.CTkFrame(self.root, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.week_frame.pack(padx=20, pady=20, fill = 'x')

        self.info_frame = ctk.CTkFrame(self.root)
        self.info_frame.pack(padx=20, pady=20, fill = 'x')

        self.conditional_frame = ctk.CTkFrame(self.root)
        self.conditional_frame.pack(padx=20, pady=20, fill = 'x')

        self.label_current_dets_heading = ctk.CTkLabel(self.info_frame, text="")
        self.label_current_dets_heading.pack(padx=10,pady=10)

        self.basic_info_frame = ctk.CTkFrame(self.info_frame, fg_color="#2b2b2b", border_width=2, border_color="#444444", corner_radius=15)
        self.basic_info_frame.pack(padx=20, pady=20, fill = 'x')

        self.desc_frame = ctk.CTkFrame(self.info_frame)
        self.desc_frame.pack(padx=20, pady=20, fill='x')

        self.label = ctk.CTkLabel(self.top_frame, text='Weather App', font=('Arial', 55))
        self.label.pack(padx=10, pady=10)

        self.check_state = ctk.IntVar()

        self.button_map = ctk.CTkButton(self.top_frame, text='Open Map', command=self.show_map, font=('Arial', 30))
        self.button_map.pack(padx=20, pady=20)

        self.button_get_fav = ctk.CTkButton(self.top_frame, text='Get Info of Fav Loc', command=self.return_favinfo, font=('Arial', 30))
        self.button_get_fav.pack(padx=20, pady=20)

        #self.day1_button = ctk.CTkButton(self.week_frame, text="Sunday", command=self.get_info, font=('Arial', 30))
        #self.day1_button.grid(row = 1, column = 0, padx=20, pady=20, sticky = 'w')


        self.label_current_temp = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_current_temp.grid(row = 1, column = 0, padx=10, pady=10, sticky='w')

        self.label_current_humidity = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_current_humidity.grid(row = 1, column = 1, padx=10, pady=10, sticky='w')

        self.label_current_description = ctk.CTkLabel(self.desc_frame, text="")
        self.label_current_description.grid(row = 2, column = 0, padx = 20, pady = 10, sticky='w')

        self.label_precip_percent = ctk.CTkLabel(self.basic_info_frame, text="")
        self.label_precip_percent.grid(row = 3, column = 0, padx=10, pady=10, sticky='w')

        self.labeL_uv_index = ctk.CTkLabel(self.basic_info_frame, text="")
        self.labeL_uv_index.grid(row = 3, column = 1, padx=10, pady=10, sticky='w')

        self.label_umbrella_check = ctk.CTkLabel(self.conditional_frame, text="")
        self.label_umbrella_check.grid(row=0, column=0, padx=10, pady=10)

        self.label_sunscreen_check = ctk.CTkLabel(self.conditional_frame, text="")
        self.label_sunscreen_check.grid(row=1, column= 0, padx=10, pady=10)

        self.root.mainloop()

    def show_map(self):
        world_map(self.root, self.return_coords)

    def return_coords(self,coords):
        print("return coords triggered", coords)
        self.place = coords
        self.get_info()

    def return_favinfo(self):

        with open('fav.txt', 'r') as f:
            data = f.read()[1:-1:1]
            data = (data).strip().split(',')
            
            lat, long = data[0], data[1].strip()
    
        self.user_selected_fav_loc = 1

        self.fav_place = (lat, long)
        self.get_info()

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
        
        #visual crossing api
        #url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{f'2025-11-{str(int(self.current_date)+1)}'}?key={self.API_KEY}"

        #visual crossing api -> with weekly stuff
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}?unitGroup=metric&key={self.API_KEY}"

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            pass
        
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

        days = self.weather_info["days"][:7]
            
        current_temp = self.weather_info['currentConditions']["temp"]
        #current_temp = (current_temp - 32)/1.8

        current_humidity = self.weather_info['currentConditions']['humidity']

        current_description = self.weather_info['description']

        current_uv_index = self.weather_info['currentConditions']['uvindex']

        current_precp_percent = self.weather_info['currentConditions']['precipprob']

        self.label_current_dets_heading.configure(text="Today's Weather is as follows : ", font=('Arial', 40))

        self.label_current_temp.configure(text=f"Current Temperature is : {current_temp:.2f} C.", font=('Arial', 30))
        self.label_current_humidity.configure(text=f"Current Humidity is : {current_humidity} percent.", font=('Arial', 30))
        self.label_current_description.configure(text=current_description, font=('Arial', 30))
        self.label_precip_percent.configure(text=f"Current Chance of Rain is : {current_precp_percent} percent.", font=('Arial', 30))
        self.labeL_uv_index.configure(text=f"Current UV Index is : {current_uv_index}.", font=('Arial', 30))
        self.label_umbrella_check.configure(text=self.umbrella_check(current_precp_percent), font=('Arial', 30))
        self.label_sunscreen_check.configure(text=self.sunscreen_check(current_uv_index), font=('Arial', 30))



class world_map:

    def __init__(self, parent, callback):

        self.callback = callback

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Map")
        self.window.geometry('1920x1080')

        self.weather_map_frame = ctk.CTkFrame(self.window)
        self.weather_map_frame.pack(side='bottom', fill='x', pady=5)

        #grid configs
        self.weather_map_frame.grid_columnconfigure(0, weight=1)
        self.weather_map_frame.grid_rowconfigure((0,1,2), weight=1)

        self.map_widget = tkintermapview.TkinterMapView(self.window, width=800, height=600, corner_radius=15)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.map_widget.set_position(12.961201, 77.590783) #default starting point of map in bangalore
        self.map_widget.set_zoom(15)
        
        self.position = None
        self.map_widget.add_left_click_map_command(self.put_marker)
        
        self.button_fav_places = ctk.CTkButton(self.weather_map_frame, text='Select Fav Places', command=self.show_fav_place_window)
        self.button_fav_places.grid(row = 3, column = 0, padx=20, pady=20)

        self.label_find_information_button = ctk.CTkButton(self.weather_map_frame, command=self.select_pos, text="Find Information")
        self.label_find_information_button.grid(row = 0, column = 0, padx = 10, pady = 10, sticky='')

        self.label_instructions = ctk.CTkLabel(self.weather_map_frame, text='Click on the place and press the button below to find information.', font=('Arial',22))
        self.label_instructions.grid(row = 1, column = 0, padx=10, pady=10, sticky = '')

        self.quit_button = ctk.CTkButton(self.weather_map_frame,text="Close Map", command=self.window.destroy)
        self.quit_button.grid(row = 2, column = 0, padx=10,pady=10, sticky = '')


    def show_fav_place_window(self):
        select_fav_places(self.window, self.return_loc_fav)

    def return_loc_fav(self, loc):
        print("return fav locs triggered")

    def put_marker(self, coords):
        print("put marker() triggered", coords)
        self.map_widget.set_marker(coords[0], coords[1], text="Selected Location")
        self.position = coords

        
    def select_pos(self):
        print("select pos() triggered", self.position)
        if self.position:
            self.callback(self.position)
            messagebox.showinfo("Info", "Weather Updated in App.")
        else:
            messagebox.showwarning("No Location", "No Location Selected.")

        
class select_fav_places:

    def __init__(self, parent, callback):

        self.callback = callback

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Select Fav Locations")
        self.window.geometry('1920x1080')


        self.fav_places_frame = ctk.CTkFrame(self.window)
        self.fav_places_frame.pack(side='bottom', fill='x', pady=5)

        self.map_widget = tkintermapview.TkinterMapView(self.window, width=800, height=600, corner_radius=15)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.fav_pos = None
        self.map_widget.add_left_click_map_command(self.put_marker)

        self.map_widget.set_position(12.961201, 77.590783) #default starting point of map in bangalore
        self.map_widget.set_zoom(15)

        self.select_fav_button = ctk.CTkButton(self.fav_places_frame, command=self.store_data, text='Set location as Fav Place.')
        self.select_fav_button.grid(row=0, column=0)


    def put_marker(self, coords):
        #print("put marker() triggered", coords)
        self.map_widget.set_marker(coords[0], coords[1], text="Selected Location")
        self.fav_pos = coords
        self.callback(self.fav_pos)

    def store_data(self):

        with open('fav.txt', 'w') as f:
            print(self.fav_pos, file=f)

        





        
        



Weather_GUI()


    





