import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city="Sydney", country_code="AU"):
    """
    Fetches current weather for a given city.
    Returns the raw JSON response as a dict.
    """
    params = {
        "q": f"{city},{country_code}",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params, timeout=15)

    if response.status_code != 200:
        raise Exception(f"OpenWeather API error {response.status_code}: {response.text}")

    return response.json()


if __name__ == "__main__":
    weather = fetch_weather("Sydney", "AU")
    print("Temperature:", weather["main"]["temp"])
    print("Conditions:", weather["weather"][0]["description"])
