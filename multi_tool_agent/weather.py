import os
import requests

OPENWEATHER_API_KEY = "c815a66682c3ce84271108a7924ec589"

def get_weather(city: str) -> dict:
    """Fetches current weather for a city using OpenWeatherMap 2.5 Weather API."""
    if not OPENWEATHER_API_KEY:
        return {"status": "error", "error_message": "API key not set."}

    # Step 1: Get coordinates for the city
    geo_url = (
        f"https://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    )
    geo_resp = requests.get(geo_url)
    if geo_resp.status_code != 200 or not geo_resp.json():
        return {"status": "error", "error_message": f"Could not find coordinates for {city}."}
    geo_data = geo_resp.json()[0]
    lat, lon = geo_data["lat"], geo_data["lon"]

    print(lon, lat)

    # Step 2: Get weather using Weather API
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    )
    weather_resp = requests.get(weather_url)
    if weather_resp.status_code != 200:
        return {"status": "error", "error_message": f"{weather_resp.status_code}: Could not fetch weather for {city} Reason: {weather_resp.text}."}
    data = weather_resp.json()
    weather_desc = data.get("weather", [{}])[0].get("description", "No data")
    temp_k = data.get("main", {}).get("temp", None)
    temp_c = round(temp_k - 273.15, 2) if temp_k is not None else "N/A"

    return {
        "status": "success",
        "report": f"The weather in {city} is {weather_desc} with a temperature of {temp_c}°C."
    }
# Example usage
if __name__ == "__main__":
    city = "London"
    weather_report = get_weather(city)
    print(weather_report)