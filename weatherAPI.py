import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Define API URL and parameters for latitude, longitude, and hourly temperature
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 44.05,      # Example coordinates (Eugene, Oregon)
    "longitude": 123.08,
    "hourly": "temperature_2m"
}

# Make the API request
responses = openmeteo.weather_api(url, params=params)

# Process the first location response
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Extract hourly temperature data
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

# Create a DataFrame with the hourly timestamps and temperatures
start_time = pd.to_datetime(hourly.Time(), unit="s", utc=True)
end_time = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True)
time_range = pd.date_range(start=start_time, end=end_time, freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left")

hourly_data = {
    "date": time_range,
    "temperature_2m": hourly_temperature_2m
}

hourly_dataframe = pd.DataFrame(data=hourly_data)

# Get today's date in UTC format (since API data is likely in UTC)
today = pd.Timestamp(datetime.utcnow().date())

# Filter the DataFrame for today's date
today_temperatures = hourly_dataframe[hourly_dataframe['date'].dt.date == today.date()]

# Convert from Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

# Print hourly temperature data for each hour today
for index, row in today_temperatures.iterrows():
    fahrenheit_temp = celsius_to_fahrenheit(row['temperature_2m'])
    print(f"Time: {row['date']} - Temperature: {round(fahrenheit_temp, 1)} °F")