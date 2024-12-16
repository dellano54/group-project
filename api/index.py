from geopy.geocoders import Nominatim
import requests
from flask import Flask, request

app = Flask(__name__)

def get_city_lat_long(city_name):
    geolocator = Nominatim(user_agent="city_locator")
    location = geolocator.geocode(city_name)
    
    
    return location.latitude, location.longitude

# Function to get weather data from Open-Meteo
def get_weather(city_name):
    coords = get_city_lat_long(city_name)
    if coords:
        latitude, longitude = coords
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code&timezone=auto&forecast_days=1"
        weather_response = requests.get(weather_url)
        
        if weather_response.status_code == 200:
            data = weather_response.json()
            w = data['daily']['weather_code'][0]
            
            return w
    return None


@app.route('/<c>')
def greet(c):
    return str(get_weather(c))

