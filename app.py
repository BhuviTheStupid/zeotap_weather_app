from flask import Flask, render_template, jsonify, request
import requests
import mysql.connector
from datetime import datetime
import threading
import time

# Flask app setup
app = Flask(__name__)

# MySQL connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2024",  # Replace with your MySQL password
    database="weather_data1"  # Replace with your database name
)
cursor = db.cursor()

# OpenWeatherMap API details
API_KEY = "8f8f17016387686cfd6722215785b8e1"  # Replace with your OpenWeatherMap API Key
CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867}
}

# Function to fetch weather data from API
def fetch_weather_data1(city, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        feels_like = data['main']['feels_like'] - 273.15  # Convert from Kelvin to Celsius
        weather = data['weather'][0]['main']
        dt = datetime.utcfromtimestamp(data['dt'])  # Convert from Unix timestamp to datetime
        return {
            "city": city,
            "temp": temp,
            "feels_like": feels_like,
            "weather": weather,
            "dt": dt
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

# Function to periodically fetch and store weather data for all cities every 5 minutes
def update_weather_data1():
    while True:
        for city, coords in CITIES.items():
            weather_data1 = fetch_weather_data1(city, coords['lat'], coords['lon'])
            if weather_data1:
                # Insert into DB with timestamp
                insert_weather_data1(
                    city,
                    weather_data1['temp'],
                    weather_data1['feels_like'],
                    weather_data1['weather'],
                    weather_data1['dt']
                )
        print("Weather data updated.")
        time.sleep(300)  # Sleep for 5 minutes before the next fetch

# Function to insert weather data into the database with timestamp
def insert_weather_data1(city, avg_temp, feels_like, dominant_condition, dt):
    query = """
        INSERT INTO daily_weather (city, avg_temp, feels_like, dominant_condition, dt)
        VALUES (%s, %s, %s, %s, %s);
    """
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(query, (city, avg_temp, feels_like, dominant_condition, dt))
    db.commit()

# Start background thread to update weather data
threading.Thread(target=update_weather_data1, daemon=True).start()

# Home Route - Dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Route for daily summary (API)
@app.route('/daily_summary', methods=['GET'])
def daily_summary():
    summary = []
    for city in CITIES.keys():
        query = "SELECT * FROM daily_weather WHERE city = %s ORDER BY dt DESC LIMIT 1"
        cursor.execute(query, (city,))
        result = cursor.fetchone()
        if result:
            summary.append({
                "city": result[1],
                "avg_temp": result[2],
                "feels_like": result[3],
                "dominant_condition": result[4],
                "dt": result[5].strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify(summary)

# Trigger alerts based on threshold
@app.route('/check_alerts', methods=['POST'])
def check_alerts():
    threshold = request.json['threshold']
    query = "SELECT city, avg_temp FROM daily_weather WHERE DATE(dt) = CURDATE()"
    cursor.execute(query)
    results = cursor.fetchall()
    alerts = []
    for result in results:
        if result[1] > threshold:
            alerts.append({
                "city": result[0],
                "temperature": result[1]
            })
    return jsonify(alerts)

if __name__ == "__main__":
    app.run(debug=True)
