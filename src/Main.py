import threading
import time
from fetch_weather import fetch_weather_data, fetch_weather_for_city
from aggregates import calculate_daily_aggregates
from alerts import generate_alerts
from database import create_tables,fetch_weather_for_city_from_db
from config import POLL_INTERVAL
from visualize import visualize_daily_summaries, visualize_alerts
from datetime import datetime

# Function to automatically fetch weather data periodically2
def auto_fetch_weather():
    while True:
        fetch_weather_data()
        time.sleep(30)  # Fetch every 30 seconds

# Function to calculate daily aggregates at specific times
def schedule_daily_aggregates():
    while True:
        now = datetime.now()
        # Check for specific times (9 AM, 12 PM, 3 PM, 6 PM, 9 PM)
        if now.hour in [9, 12, 15, 18, 21] and now.minute == 0:
            calculate_daily_aggregates()
            print(f"Daily aggregates calculated at {now.strftime('%H:%M')}.")
            time.sleep(60)  # Wait for a minute to avoid multiple triggers
        time.sleep(30)  # Check every 30 seconds

def main():
    create_tables()  # Ensure database tables are created

    # Start the background thread for automatic weather fetching
    weather_thread = threading.Thread(target=auto_fetch_weather)
    weather_thread.daemon = True
    weather_thread.start()

    # Start the background thread for scheduling daily aggregates
    aggregates_thread = threading.Thread(target=schedule_daily_aggregates)
    aggregates_thread.daemon = True
    aggregates_thread.start()

    while True:
        print("\n1. Fetch current weather for a specific city")
        print("2. Visualize daily summaries")
        print("3. Visualize alerts")
        print("4. View weather data for a specific city")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Fetch current weather for a specific city
            city = input("Enter the city name: ")
            weather_data = fetch_weather_for_city(city)
            if weather_data:
                print(f"\nCurrent weather in {city}:")
                print(f"Main: {weather_data['weather'][0]['main']}")
                print(f"Temperature: {weather_data['main']['temp']}°C")
                print(f"Feels Like: {weather_data['main']['feels_like']}°C")
                print(f"Humidity: {weather_data['main']['humidity']}%")
                print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
                print(f"Timestamp: {weather_data['dt']}")
            else:
                print(f"No data available for {city} at this moment.")

        elif choice == '2':
            # Visualize daily summaries
            print("Visualizing daily summaries...")
            visualize_daily_summaries()

        elif choice == '3':
            # Visualize alerts
            print("Visualizing alerts...")
            visualize_alerts()

        elif choice == '4':
            # View weather data for a specific city
            city = input("Enter the city name: ")
            # Fetch and display data from the database
            data = fetch_weather_for_city_from_db(city)  # Implement this in your database.py
            if data:
                print(f"\nWeather data for {city}: {data}")
            else:
                print(f"No data available for {city}.")

        elif choice == '5':
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
