# Weatherly - Weather Prediction App

## Description
### Python Jackfruit Problem: <br>
A simple weather app written in Python using CustomTkinter for the GUI and the Visual Crossing Weather API for live weather data. 

## Video Demo
https://github.com/user-attachments/assets/87a51143-fecd-49e4-8d9f-188fecb02bdc <br>
Screenshots of the different windows are available in the "readme_assets" folder.

## Installation

Clone the repo into your device:

```bash
git clone https://github.com/NorSomething/Weather-App.git
```

### Install the required python modules:

It is recommended to create a virtual environment in the app's directory using the ```venv``` python module.
```bash
python -m venv <your venv name>
```
And to activate the above said virtual environment:
```bash
source <your venv name>/bin/activate
```
To install the modules:
```bash
pip install -r requirements.txt
```

## Usage

An API key from ```https://www2.visualcrossing.com/weather-api/``` is required for the working of the app. 
Store the API key in a .env file in the format ```API_KEY=<your api key>``` in the same folder as the app.

Run the app with:
``` py 
python main.py 
```
### Note:
As of now, the app works best with scaling set to 100% on a 1920x1080p display.


## Contributors

M C Nirmal Kumar - PES2202502154 <br>
Ananya Samaga - PES2202502164​ <br>
Dhruti Jayaprakash Bharadwaj - PES2202502325 <br>
Chaitra Govindaraju - PES2202502219 <br>


## ToDo:
- [x] Main GUI
- [x] Fav Location Saving
- [x] Multiple Windows
- [x] Beautify GUI
- [x] Weekly Data
- [x] Graphs
- [x] Sunrise Moonphase
- [ ] AQI
- [x] Loading Spinner
- [ ] Initial Loading Screen
- [x] UX Improvements
- [ ] Auto Scaling to Display
