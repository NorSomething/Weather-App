import customtkinter as ctk
import tkinter
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

class weekly_stats:

    def __init__(self, parent, weather_json, data_list):

        self.weather_json = weather_json
        self.data_list = data_list
        
        self.weekly_stats_window = ctk.CTkToplevel(parent)
        self.weekly_stats_window.title("Statistics Window")
        self.weekly_stats_window.geometry('1920x1080')

        print("Min Temperature List : ",self.data_list[1])

        self.button_test = ctk.CTkButton(self.weekly_stats_window, text='test', command=self.get_graph, font=('Arial', 30))
        self.button_test.pack(padx=20, pady=20)

    def get_graph(self):
        xpoints = np.array(self.data_list[0])
        ypoints = np.array(self.data_list[1])
        plt.plot(xpoints, ypoints)
        plt.show()

        