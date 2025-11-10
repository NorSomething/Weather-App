import requests
import tkinter
import customtkinter as ctk
import tkintermapview
import os
import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from dotenv import load_dotenv

import fav_place

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
        fav_place.select_fav_places(self.window, self.return_loc_fav)

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

