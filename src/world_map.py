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

    def __init__(self, parent, pos):

        self.pos = pos #this is storing return_coords() from main.py

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Map")
        self.window.geometry('1350x1020')
        self.window.configure(fg_color="#101010")

        self.weather_map_frame = ctk.CTkFrame(self.window,fg_color="#101010")
        self.weather_map_frame.pack(padx=10, pady=10, side='bottom', fill='x')

        #grid configs
        self.weather_map_frame.grid_columnconfigure((0,1), weight=1)
        self.weather_map_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.map_widget = tkintermapview.TkinterMapView(self.weather_map_frame, width=1280, height=720, corner_radius=15)
        #self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.map_widget.grid(row = 0, column=0, padx=10, pady=10)

        self.map_widget.set_position(12.961201, 77.590783) #default starting point of map in bangalore
        self.map_widget.set_zoom(15)
        
        self.position = None
        self.map_widget.add_left_click_map_command(self.put_marker)
        


        self.label_find_information_button = ctk.CTkButton(self.weather_map_frame, command=self.select_pos, text="Find Information", font=('Arial', 30),fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.label_find_information_button.grid(row = 1, column = 0, padx=10, pady=10)

        self.quit_button = ctk.CTkButton(self.weather_map_frame,text="Close Map", command=self.window.destroy, font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.quit_button.grid(row = 3, column = 0, padx=10, pady=10)

        self.button_fav_places = ctk.CTkButton(self.weather_map_frame, text='Select Fav Places', command=self.show_fav_place_window, font=('Arial', 30), fg_color="#4A90E2", hover_color="#3A78C2", text_color="white")
        self.button_fav_places.grid(row = 2, column = 0, padx=10, pady=10)

        self.label_instructions = ctk.CTkLabel(self.weather_map_frame, text='Click on the place and press the button below to find information.', font=('Arial',30), wraplength=1280, justify='center')
        self.label_instructions.grid(row = 4, column = 0, padx=10, pady=10)


    def show_fav_place_window(self):
        fav_place.select_fav_places(self.window)

    def put_marker(self, coords):
        print("put marker() triggered", coords)
        self.map_widget.set_marker(coords[0], coords[1], text="Selected Location")
        self.position = coords

        
    def select_pos(self):
        print("select pos() triggered", self.position)
        if self.position:
            self.pos(self.position) #calling return_coords(position)
            messagebox.showinfo("Info", "Weather Updated in App.")
        else:
            messagebox.showwarning("No Location", "No Location Selected.")

