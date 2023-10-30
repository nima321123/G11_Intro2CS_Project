import requests
import datetime as dt
import tkinter as tk

class Task1:
    def get_weather():
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        API_KEY = "c9e9db60a93f15a43de916d49d078ae9" 
        CITY = city_entry.get() #obtain the city entered in the Entry Widget 

        # Make a request to the weather API
        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url)
        data = response.json()

        # Extract weather information from the API response
        if data['cod'] == 200: #sucessful response
            city_name = data['name']
            temp_kelvin = data['main']['temp']
            temp_celsius = temp_kelvin - 273.15
            feels_like_kelvin = data['main']['feels_like']
            feels_like_celsius = feels_like_kelvin - 273.15
            wind_speed = data['wind']['speed']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            sunrise_time = dt.datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
            sunset_time = dt.datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

            # Update the label with the weather information
            weather_label.config(text=f"City: {city_name}\nTemperature: {temp_celsius:.2f}°C\nFeels like: {feels_like_celsius:.2f}°C\nGeneral weather: {description}\nHumidity: {humidity}%\nWind speed: {wind_speed}m/s\nSun rise at {sunrise_time} local time\n Sun sets at {sunset_time} local time")
        else:
            weather_label.config(text="Invalid city name")

root = tk.Tk()
root.title('Weather API')
root.geometry('300x300')

# Create and pack the city entry field
city_entry = tk.Entry(root)
city_entry.pack()

# Create the weather label
weather_label = tk.Label(root)
weather_label.pack()

# Create the button to fetch weather data
weather_button = tk.Button(root, text="Get Weather", command=Task1.get_weather)
weather_button.pack()

root.mainloop()