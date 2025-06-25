Multi Tool Weather Agent

This project provides a Python agent that fetches current weather information for a given city using the OpenWeatherMap API and suggests what to wear or take when traveling, powered by an LLM.

## Features

- Fetches real-time weather data for any city.
- Uses an LLM to generate travel/clothing suggestions based on weather.
- Simple API for integration or extension.

## Setup

1. Install dependencies:
   ```
   pip install requests
   ```
2. Set your OpenWeatherMap API key:
   ```
   export OPENWEATHER_API_KEY=your_api_key
   ```
3. (Optional) Configure your LLM integration.

## Usage

Import and use the agent in your Python code:

```python
from multi_tool_agent.agent import get_weather

# Replace `llm` with your LLM client instance
result = get_weather("London", llm=your_llm)
print(result)
```

## License

MIT License.