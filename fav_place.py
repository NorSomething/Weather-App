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

class select_fav_places:

    def __init__(self, parent, callback):

        self.callback = callback

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Select Fav Locations")
        self.window.geometry('1920x1080')


        self.fav_places_frame = ctk.CTkFrame(self.window)
        self.fav_places_frame.pack(side='bottom', fill='x', pady=5)

        self.fav_places_frame.columnconfigure((0,1,2,3), weight=1)
        self.fav_places_frame.rowconfigure((0), weight=1)

        self.map_widget = tkintermapview.TkinterMapView(self.window, width=800, height=600, corner_radius=15)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.fav_pos = None
        self.map_widget.add_left_click_map_command(self.put_marker)

        self.map_widget.set_position(12.961201, 77.590783) #default starting point of map in bangalore
        self.map_widget.set_zoom(15)

        #passing lambda funcition here cuz command cant take functions with parameters
        self.select_fav_button1 = ctk.CTkButton(self.fav_places_frame, command= lambda : self.store_data("fav_place1"), text='Set location as Fav Place 1')
        self.select_fav_button1.grid(row=0, column=0)

        self.select_fav_button2 = ctk.CTkButton(self.fav_places_frame, command= lambda : self.store_data("fav_place2"), text='Set location as Fav Place 2')
        self.select_fav_button2.grid(row=0, column=1)
        
        self.select_fav_button3 = ctk.CTkButton(self.fav_places_frame, command= lambda : self.store_data("fav_place3"), text='Set location as Fav Place 3')
        self.select_fav_button3.grid(row=0, column=2)

        self.select_fav_button4 = ctk.CTkButton(self.fav_places_frame, command= lambda : self.store_data("fav_place4"), text='Set location as Fav Place 4')
        self.select_fav_button4.grid(row=0, column=3)


    def put_marker(self, coords):
        self.map_widget.set_marker(coords[0], coords[1], text="Selected Location")
        self.fav_pos = coords
        self.callback(self.fav_pos)

    def store_data(self, fav_key):

        try:
            with open('fav_places.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = dict()

        data[fav_key] = self.fav_pos

        with open('fav_places.json', 'w') as f:
            json.dump(data, f, indent=4)


