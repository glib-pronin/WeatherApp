import requests, colorama
from .get_env_data import api_key

colorama.init(autoreset=True)

def get_weather(city_name: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ua'
    response = requests.get(url=url)
    if response.status_code==200:
        return response.json() 
    else:
        red = colorama.Fore.RED
        print(f"{red}Error, get data")