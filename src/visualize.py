import sqlite3
from config import DB_PATH
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

def visualize_daily_summaries():
    """Fetch and visualize the most recent daily summaries for each city as a line plot."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Modified SQL query to fetch only the latest data for each city on a given day
    cursor.execute('''
    SELECT city, avg_temperature, max_temperature, min_temperature, date 
    FROM daily_aggregates
    WHERE id IN (
        SELECT MAX(id) 
        FROM daily_aggregates 
        GROUP BY city, date
    )
    ''')
    
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No daily aggregate data available for visualization.")
        return

    cities = []
    avg_temps = []
    max_temps = []
    min_temps = []

    for row in data:
        city, avg_temp, max_temp, min_temp, date = row
        cities.append(city)
        avg_temps.append(avg_temp)
        max_temps.append(max_temp)
        min_temps.append(min_temp)

    # Create line plots for visualization
    x = range(len(cities))  # X-axis values for each city

    plt.figure(figsize=(12, 6))
    
    # Plotting the temperature lines with markers
    plt.plot(x, avg_temps, 'bo-', label='Average Temperature', linewidth=2, markersize=8)
    plt.plot(x, max_temps, 'ro-', label='Max Temperature', linewidth=2, markersize=8)
    plt.plot(x, min_temps, 'go-', label='Min Temperature', linewidth=2, markersize=8)

    # Customizing the plot
    plt.xlabel('Cities')
    plt.ylabel('Temperature (°C)')
    plt.title('Daily Temperature Summaries')
    plt.xticks(x, cities, rotation=45, ha='right')  # X-axis labels
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()  # Adjust layout to prevent label cutoff

    # Show the plot
    plt.show()

if __name__ == "__main__":
    visualize_daily_summaries()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from config import DB_PATH

def visualize_alerts():
    """Fetch and visualize weather alerts."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fetch the alert data
    cursor.execute('SELECT city, alert_type, value, timestamp FROM alerts')
    alerts = cursor.fetchall()
    conn.close()

    # If no alerts, print message
    if not alerts:
        print("No alerts available.")
        return
    
    # Convert alerts to pandas DataFrame for easier visualization
    df = pd.DataFrame(alerts, columns=['City', 'Alert Type', 'Value', 'Timestamp'])
    
    # Group by alert type and count occurrences for visualization
    alert_counts = df['Alert Type'].value_counts()
    
    # Plot the alert counts
    plt.figure(figsize=(10, 6))
    alert_counts.plot(kind='bar', color='skyblue')
    plt.title('Weather Alerts Count by Type')
    plt.xlabel('Alert Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
