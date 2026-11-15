
import requests
import pandas as pd

def extract_weather():

    URL = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 33.5731,
        "longitude": -7.5898,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "timezone": "Africa/Casablanca",
        "forecast_days": 7
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["hourly"])
    df["city"] = "Casablanca"

    print("Extraction completed!")
    print("Total records:", len(df))

    return df


if __name__ == "__main__":
    df = extract_weather()
    
