# alerts.py
from config import ALERT_THRESHOLD
from database import store_alert

def generate_alerts(weather_data):
    """Generate alerts if thresholds are breached (e.g., temperature > threshold)."""
    city = weather_data['name']
    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    
    if temp > ALERT_THRESHOLD['temperature_max']:
        store_alert(city, 'temperature_max', temp)
    if wind_speed > ALERT_THRESHOLD['wind_speed_max']:
        store_alert(city, 'wind_speed_max', wind_speed)
