import sqlite3
from config import DB_PATH
from tabulate import tabulate  # Import tabulate for table formatting

def fetch_all_weather_data():
    """Fetch and display all stored weather data in a tabular format."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM weather_data")
    rows = cursor.fetchall()

    # Define table headers (based on the columns in your weather_data table)
    headers = ["ID", "City", "Main", "Temperature", "Feels Like", "Humidity", "Wind Speed", "Timestamp"]

    # Use tabulate to display the data in a table format
    print(tabulate(rows, headers, tablefmt="grid"))

    conn.close()

if __name__ == "__main__":
    fetch_all_weather_data()
