import sqlite3
from config import DB_PATH
import datetime
from database import store_daily_aggregates

def calculate_daily_aggregates():
    """Calculate and store daily aggregates (avg, max, min temperature, dominant condition) for each city."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Update the query to use 'temp' instead of 'temperature'
    cursor.execute('''
    SELECT city, AVG(temp), MAX(temp), MIN(temp), 
                   main as dominant_condition, COUNT(main)
    FROM weather_data
    GROUP BY city, date(timestamp)
    ''')
    
    results = cursor.fetchall()

    for row in results:
        city, avg_temp, max_temp, min_temp, dominant_condition, _ = row
        store_daily_aggregates(city, avg_temp, max_temp, min_temp, dominant_condition)
    
    
    conn.commit()
    conn.close()
