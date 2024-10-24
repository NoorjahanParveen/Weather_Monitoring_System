# fetch_weather.py
import requests
from config import API_KEY, BASE_URL, CITIES
from database import store_weather_data

def fetch_weather_data():
    """Fetch weather data for all metro cities in India and store it in the database."""
    for city in CITIES:
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            store_weather_data(data)
        else:
            print(f"Failed to fetch data for {city} (status code: {response.status_code})")

def fetch_weather_for_city(city):
    """Fetch weather data for a specific city from OpenWeather API."""
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {city} (status code: {response.status_code})")
        return None
