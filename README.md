[![Status](https://img.shields.io/badge/status-active-success.svg)]() [![GitHub Issues](https://img.shields.io/github/issues/TheBugYouCantFix/WeatherApp)](https://github.com/TheBugYouCantFix/WeatherApp/issues) ![Lines of code](https://img.shields.io/tokei/lines/github/TheBugYouCantFix/WeatherApp)

# WeatherApp

## Content
- [Brief description](#brief-description)
- [Tools](#tools)
- [Features](#features)
- [Hotkeys](#hotkeys)
- [How it works](#how-it-works)
- [Screenshots](#screenshots)
- [Ways to improve the project](#ways-to-improve-the-project)
- [Installation](#installation)

## Brief description
This GUI app was created to show the detailed information about the weather in any city selected by user.

## Tools
**Language:** *Python*</br>
**API:** *[OpenWeather](https://openweathermap.org/)*

**Libraries:** 
  - [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
  - [qt_material](https://pypi.org/project/qt-material/)
  - [requests](https://docs.python-requests.org/en/latest/)
      - **Built-in libraries**:
        - [sqlite3](https://docs.python.org/3/library/sqlite3.html)
        - [functools](https://docs.python.org/3/library/functools.html)
        - [ctypes](https://docs.python.org/3/library/ctypes.html)
  
## Features
<ul>
    <li>Settings</li>
    <li>Favorite cities</li>
    <li>App can be minimized to tray</li>
    <li>Hotkeys</li>
    <li>The search works for both Latin and Cyrillic alphabet</li>
</ul>

## Hotkeys
<ul>
    <li>Enter: search</li>
    <li>Shift + F1: favorites & back</li>
    <li>Shift + F2: settings & back</li>
</ul>

## How it works
The app parses the data from [OpenWeather API](https://openweathermap.org/) and displays them to the main window.<br>
QStackedWidget is used to switch between all 3 windows of the app. <br>
Favorite cities and settings are stored into the sqlite databases. <br>


##Screenshots
<p>Main window<br> <img src="https://i.ibb.co/9NnVRXx/image.png"> <br></p>
<p>Settings window<br> <img src="https://i.ibb.co/XzpQd5P/image.png"> <br></p>
<p>Favorites window<br> <img src="https://i.ibb.co/KWCPLN6/image.png"> <br></p>

## Ways to improve the project
<ul>
    <li>Add accounts for every user to personalize the usage of the app</li>
    <li>Add forecast for a chosen time span(day, week, etc.)</li>
    <li>Use threads</li>
    <li>Make functions asynchronous using <b>asyncio</b> module</li>
</ul>

## Installation
```
git clone https://github.com/TheBugYouCantFix/WeatherApp.git
cd WeatherApp
pip install -r requirements.txt
```
Get your token [here](https://openweathermap.org/price)

Open **weather_parsing** folder. Then go to **config.py** and insert your token into the **TOKEN** variable.
```
python main.py
```
