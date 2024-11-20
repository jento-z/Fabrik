import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 44.05,  # Example coordinates (Eugene, Oregon)
        "longitude": 123.08,
        "hourly": "temperature_2m",
        "current_weather": True,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        current_temp_celsius = data.get("current_weather", {}).get("temperature")
        if current_temp_celsius is not None:
            # Convert from Celsius to Fahrenheit
            current_temp_fahrenheit = round((current_temp_celsius * 9/5) + 32, 1)
            return current_temp_fahrenheit
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
