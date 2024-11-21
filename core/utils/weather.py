import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 44.05,  # Example coordinates (Eugene, Oregon)
        "longitude": -123.08,
        "hourly": "temperature_2m,precipitation,cloudcover",  # Request hourly temperature, precipitation, and cloud cover
        "current_weather": True,  # Fetch current weather details
        "timezone": "auto",  # Automatically adjusts timezone
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Extract hourly data
        hourly_temperatures = data.get("hourly", {}).get("temperature_2m", [])
        hourly_precipitation = data.get("hourly", {}).get("precipitation", [])
        hourly_cloudcover = data.get("hourly", {}).get("cloudcover", [])

        # Extract current temperature
        current_temp_celsius = data.get("current_weather", {}).get("temperature")
        current_temp_fahrenheit = (
            round((current_temp_celsius * 9/5) + 32, 1)
            if current_temp_celsius is not None else None
        )

        # Find the high temperature for the day (convert to Fahrenheit)
        if hourly_temperatures:
            daily_high_celsius = max(hourly_temperatures)
            daily_high_fahrenheit = round((daily_high_celsius * 9/5) + 32, 1)
        else:
            daily_high_fahrenheit = None

        # Determine average cloud cover and precipitation for the day
        average_cloudcover = sum(hourly_cloudcover) / len(hourly_cloudcover) if hourly_cloudcover else 0
        is_raining_today = any(precip > 0 for precip in hourly_precipitation)

        # Weather classification
        if average_cloudcover < 25 and not is_raining_today:
            weather_classification = "Sunny"
        elif 25 <= average_cloudcover <= 70 and not is_raining_today:
            weather_classification = "Sun with Cloud Cover"
        elif 25 <= average_cloudcover <= 70 and is_raining_today:
            weather_classification = "Sun with Cloud Cover and Rain"
        elif average_cloudcover > 70 and is_raining_today:
            weather_classification = "Cloud Cover and Rain"
        else:
            weather_classification = "Cloud Cover"

        # Output results
        weather_info = {
            "current_temperature_fahrenheit": current_temp_fahrenheit,
            "daily_high_fahrenheit": daily_high_fahrenheit,
            "weather_classification": weather_classification
        }

        print(weather_info)
        return weather_info
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None