import requests, colorama
from .env_data import api_key_w_map, api_key_w_api

colorama.init(autoreset=True)

def get_weather(city_name: str, forecast_type: str):
    """
    forecast_type:
        - "current" - current weather
        - "forecast" - forecast for several days
        - "daily" - forecast for current day
    """
    print(city_name)
    red = colorama.Fore.RED
    if forecast_type == "current":
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key_w_map}&units=metric&lang=ua'
    elif forecast_type == "forecast":
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key_w_map}&units=metric&lang=ua'
    elif forecast_type == "daily":
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key_w_api}&q={city_name}&days=1&aqi=no&alerts=no'
    else:
        print(f"{red}Error, incorrect forecast type")
        return None
    response = requests.get(url=url)
    if response.status_code==200:
        return response.json() 
    else:
        print(f"{red}Error, get data")
