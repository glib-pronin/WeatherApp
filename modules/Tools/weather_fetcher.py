import requests, colorama
from .env_data import api_key_w_map, api_key_w_api, user_name

colorama.init(autoreset=True)

def get_weather(city_name: str, forecast_type: str, lang: str = "ua"):
    """
    forecast_type:
        - "current" - current weather
        - "forecast" - forecast for several days
        - "daily" - forecast for current day
    """
    print(city_name)
    red = colorama.Fore.RED
    if forecast_type == "current":
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key_w_map}&units=metric&lang={lang}'
    elif forecast_type == "forecast":
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key_w_map}&units=metric'
    elif forecast_type == "daily":
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key_w_api}&q={city_name}&days=1&aqi=no&alerts=no'
    else:
        print(f"{red}Error, incorrect forecast type")
        return None
    print(url)
    response = requests.get(url=url)
    if response.status_code==200:
        return response.json() 
    else:
        print(f"{red}Error, get data")

def get_translated_city_name(city_name: str):
    url = f'http://api.geonames.org/searchJSON?q={city_name}&lang=uk&maxRows=1&username={user_name}'
    response = requests.get(url)
    data =  response.json()
    if data["geonames"]:
        return [data["geonames"][0]["name"], data["geonames"][0]["toponymName"]]
    return []