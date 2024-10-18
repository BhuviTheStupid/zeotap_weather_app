# zeotap_weather_app
# Real-Time Weather Monitoring Dashboard

This repository contains a **Real-Time Weather Monitoring Dashboard**, which fetches and displays weather data, temperature trends, and alerts for multiple cities using the OpenWeatherMap API. The system supports dynamic data fetching, unit conversions, and customizable temperature alerts. It is built using Python, HTML, CSS, JavaScript, MySQL, and various third-party libraries.

## Features

- **Real-Time Weather Summary**: Displays the current weather for multiple cities.
- **Temperature Unit Conversion**: Users can toggle between Celsius, Fahrenheit, and Kelvin.
- **Temperature Trends**: A bar chart shows temperature trends across cities.
- **Custom Alerts**: Users can set a temperature threshold to receive alerts when the threshold is exceeded in any city.
- **Responsive Design**: Fully responsive, mobile-friendly interface.

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap), JavaScript (Chart.js)
- **Backend**: Python (Flask)
- **API**: OpenWeatherMap API
- **Database**: MySQL for storing and retrieving weather data

## How to Run

### Prerequisites
- Python 3.x
- MySQL
- Node.js (for local hosting of frontend)
- [OpenWeatherMap API Key](https://openweathermap.org/api)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather-dashboard.git
   cd weather-dashboard
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database and modify the connection details in `app.py`.

4. Get your OpenWeatherMap API key and set it in the environment variables.

5. Run the Flask app:
   ```bash
   python app.py
   ```

6. Open `index.html` in your browser or use a local server to view the dashboard.

### Database Structure

The application uses MySQL to store weather data for multiple cities. The database structure is simple but scalable to support real-time monitoring and future enhancements.

- **Database Name**: `weather_dashboard`

- **Tables**:
  1. **cities**
     - **city_id** (INT, Primary Key, Auto Increment): Unique ID for each city.
     - **city_name** (VARCHAR(100)): The name of the city being monitored.
     - **country** (VARCHAR(50)): The country to which the city belongs.
  
  2. **weather_data**
     - **data_id** (INT, Primary Key, Auto Increment): Unique ID for each weather data entry.
     - **city_id** (INT, Foreign Key): The ID of the city from the `cities` table.
     - **avg_temp** (FLOAT): The average temperature in Kelvin.
     - **feels_like** (FLOAT): The "feels like" temperature in Kelvin.
     - **dominant_condition** (VARCHAR(50)): The dominant weather condition (e.g., Clear, Rain).
     - **date_time** (DATETIME): The timestamp for the weather data.

  3. **alerts**
     - **alert_id** (INT, Primary Key, Auto Increment): Unique ID for each alert.
     - **city_id** (INT, Foreign Key): The ID of the city from the `cities` table.
     - **threshold_temp** (FLOAT): The temperature threshold set by the user.
     - **alert_message** (TEXT): The alert message generated when the threshold is crossed.

### Relationships:

- The `cities` table is linked to the `weather_data` table via `city_id`, allowing weather data to be associated with specific cities.
- The `alerts` table is linked to the `cities` table via `city_id` to trigger notifications when specific conditions are met for a particular city.

This structure allows the app to efficiently store, retrieve, and process weather data for multiple cities and manage user-defined alerts.

### File Structure

- `app.py`: Backend server for handling API requests and data processing.
- `index.html`: Main frontend interface displaying the dashboard and weather data.
- `static/`: Directory containing JavaScript, CSS, and other static assets.
- `templates/`: Contains HTML templates for rendering the frontend.

### Available API Endpoints

- **GET /daily_summary**: Retrieves daily weather summary for all cities.
- **POST /add_city**: Adds a new city to the weather monitoring list.

## Screenshots

![image](https://github.com/user-attachments/assets/5f460f35-ad00-4ccb-aa4b-a7d16c553ee3)

Options for temperature selection
![image](https://github.com/user-attachments/assets/8eb833dc-6c2a-4346-ae5e-6c0082ed6e07)


## License

This project is licensed under the MIT License.
