import requests
import datetime


def get_current_weather_data(city: str, token: str, units='metric'):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units={units}"
        get_request = requests.get(url)

        data = get_request.json()

        weather_map = {
            "temperature": round(data["main"]["temp"]),
            "feels like": round(data["main"]["feels_like"]),

            "max temperature": round(data["main"]["temp_max"]),
            "min temperature": round(data["main"]["temp_min"]),

            "city": data["name"],
            "country": data["sys"]["country"],

            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],

            "wind speed": round(data["wind"]["speed"], 1),
            "wind azimuth": data["wind"]["deg"],

            "sunrise time": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]),
            "sunset time": datetime.datetime.fromtimestamp(data["sys"]["sunset"]),

            "description": data["weather"][0]["description"],
            "icon url": f'http://openweathermap.org/img/wn/{data["weather"][0]["icon"]}@2x.png'
        }

        day_length = weather_map["sunset time"] - weather_map["sunrise time"]
        h, m = str(day_length)[:-3].split(':')
        weather_map["day length"] = f"{h} hours, {m} minutes"

        weather_map["sunrise time"] = f'{weather_map["sunrise time"].strftime("%H:%M")} UTC'
        weather_map["sunset time"] = f'{weather_map["sunset time"].strftime("%H:%M")} UTC'

    except requests.ConnectionError as ce:
        print(ce)
        return "Check your internet connection"
    except Exception as e:
        print(f"Error: {e}")
        return "Invalid input"
    else:
        return weather_map

