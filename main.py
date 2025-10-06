import requests
import tkinter as tk
import os
from tkinter import messagebox
from tkinter import PhotoImage
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv('API_KEY')
print("Loaded API Key :", API_KEY)

city = input("Enter City : ")

def get_weather_data(ci):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ci}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        pass



weather_info = get_weather_data(city)

if weather_info:
    print(f"Current Temperature is {weather_info['main']['temp']} Celcius.")
    print(f"Pressure is {weather_info['main']['pressure']} bar.")
    print(f"Humidity is {weather_info['main']['humidity']} percent.")
    print(f"Wind speed is {weather_info['wind']['speed']} km/h.")
else:
    print(f"Unable to fetch weather info for {city}.")


    





