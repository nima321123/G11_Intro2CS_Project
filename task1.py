class Task1:
    import datetime as dt
    import requests 

    #define the URL
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "c9e9db60a93f15a43de916d49d078ae9"
    CITY = "Ho Chi Minh City, VN"

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()
    
    #function to convert temperature unit
    def kelvin_to_celsius_fahrenheit(kelvin):
        celsius = kelvin - 273.15
        return celsius

    #get data from response in API
    temp_kelvin = response['main']['temp']
    temp_celsius = kelvin_to_celsius_fahrenheit(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    wind_speed = response['wind']['speed'] 
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']) 
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    
    #print weather information of a city
    print(f"Temperature in {CITY}: {temp_celsius:.2f}°C")
    print(f"Temperature in {CITY} feels link: {feels_like_celsius:.2f}°C")
    print(f"Humidity in {CITY}: {humidity}%")
    print(f"Wind Speed in {CITY}: {wind_speed}m/s")
    print(f"General Weather in {CITY}: {description}")
    print(f"Sun rise in {CITY} at {sunrise_time} local time.")
    print(f"Sun sets in {CITY} at {sunset_time} local time.")


    

    