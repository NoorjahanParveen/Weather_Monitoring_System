# database.py
import sqlite3
from config import DB_PATH

def create_tables():
    """Create tables to store weather data and daily aggregates."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop the old table if it exists (Be careful with data!)
    cursor.execute('DROP TABLE IF EXISTS weather_data')

    # Create the updated table with the new schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY,
        city TEXT,
        main TEXT,  -- Main weather description
        temp REAL,  -- Current temperature
        feels_like REAL,  -- Feels like temperature
        humidity REAL,  -- Humidity percentage
        wind_speed REAL,  -- Wind speed in meters per second
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # No changes to the other tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_aggregates (
        id INTEGER PRIMARY KEY,
        city TEXT,
        avg_temperature REAL,
        max_temperature REAL,
        min_temperature REAL,
        dominant_condition TEXT,
        date DATE
    )
    ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS daily_aggregates (
        id INTEGER PRIMARY KEY,
        city TEXT,
        avg_temperature REAL,
        max_temperature REAL,
        min_temperature REAL,
        dominant_condition TEXT,
        date DATE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY,
        city TEXT,
        alert_type TEXT,
        value REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


def store_weather_data(data):
    """Store fetched weather data into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert new weather fields into the database
    cursor.execute('''
    INSERT INTO weather_data (city, main, temp, feels_like, humidity, wind_speed)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],  # city
        data['weather'][0]['main'],  # main weather condition
        data['main']['temp'],  # current temperature
        data['main']['feels_like'],  # feels like temperature
        data['main']['humidity'],  # humidity
        data['wind']['speed']  # wind speed
    ))
    
    conn.commit()
    conn.close()


def fetch_weather_for_city_from_db(city):
    """Fetch weather data for a specific city from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM weather_data WHERE city = ? ORDER BY timestamp ''', (city,))
    data = cursor.fetchone()
    conn.close()
    return data



def store_alert(city, alert_type, value):
    """Store an alert into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO alerts (city, alert_type, value)
    VALUES (?, ?, ?)
    ''', (city, alert_type, value))
    conn.commit()
    conn.close()

def store_daily_aggregates(city, avg_temperature, max_temperature, min_temperature, dominant_condition):
    """Store daily aggregates into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' 
    INSERT INTO daily_aggregates (city, avg_temperature, max_temperature, min_temperature, dominant_condition, date)
    VALUES (?, ?, ?, ?, ?, date('now'))
    ''', (city, avg_temperature, max_temperature, min_temperature, dominant_condition))
    conn.commit()
    conn.close()
