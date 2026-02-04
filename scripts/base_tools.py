import os 
from langchain.tools import tool
import requests
import ollama

@tool
def web_search(query: str):
    """
    Perform a live web search using Ollama Web Search API

    Input: 
        query: search a query string

    Output: 
        JSON string of top results (max_results=2)
    """
    response = ollama.web_search(query=query, max_results=2)
    response = response.results
    return response

@tool 
def get_weather(location: str):
    """Get current weather for the location using Weather.API

    Use for queries about weather, temperature or conditions in any city
    Example: "weather in Paris", "temperature in Tokyo", "is it raining in London"

    Args: 
        location: City name (e.g., "New York", "London")

    Returns:
        Current weather including temperature and conditions
    """

    url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv("WEATHER_API_KEY")}&q={location}&aqi=no"
    response = requests.get(url=url, timeout=10)
    response.raise_for_status()

    data = response.json()
    
    return data 