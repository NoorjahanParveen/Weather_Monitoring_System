import os

API_KEY = "9d17fca8edfc527d5032abb0e71b4a27"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
CITIES = ["Mumbai", "Delhi", "Kolkata", "Chennai", "Bangalore", "Hyderabad", "Ahmedabad", "Pune"]

# Update the DB_PATH to point to the 'data' folder
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'weather_data.db')

POLL_INTERVAL = 5  # 5 minutes (300 seconds)
ALERT_THRESHOLD = {
    'temperature_max': 40,  # Example threshold
    'wind_speed_max': 20
}

