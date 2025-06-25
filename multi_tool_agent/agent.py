# multi_tool_agent/agent.py
import os
import requests
from google.adk.agents import Agent

import os
import requests
import litellm

OPENWEATHER_API_KEY = "PROVIDE_THE_KEY"

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

    prompt = (
        f"The weather in {city} is {weather_desc} with a temperature of {temp_c}°C. "
        "What should a traveler wear or take when visiting?"
    )
    # Use litellm to call Ollama
    suggestion = litellm.completion(
        model="ollama/phi3:latest",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
    return {
        "status": "success",
        "report": f"The weather in {city} is {weather_desc} with a temperature of {temp_c}°C.",
        "suggestion": suggestion
    }

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about the weather in a city.",
    instruction="You are a helpful agent who can answer user questions about the weather in a city.",
    tools=[get_weather],
)