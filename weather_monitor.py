import requests
import schedule
import time
from datetime import datetime
import sqlite3

API_KEY = '9d17fca8edfc527d5032abb0e71b4a27'  # Replace with your OpenWeatherMap API key
CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]  # Add more cities as needed
DATABASE = 'weather_data.db'

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def store_weather_data(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Weather (
            id INTEGER PRIMARY KEY,
            city TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            main_condition TEXT,
            timestamp DATETIME
        )
    ''')
    cursor.execute('''
        INSERT INTO Weather (city, temperature, humidity, wind_speed, main_condition, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['main']['temp'], data['main']['humidity'], data['wind']['speed'], data['weather'][0]['main'], datetime.now()))
    conn.commit()
    conn.close()

def fetch_and_store_weather():
    for city in CITIES:
        weather_data = get_weather_data(city)
        store_weather_data(weather_data)

schedule.every(5).minutes.do(fetch_and_store_weather)

while True:
    schedule.run_pending()
    time.sleep(1)