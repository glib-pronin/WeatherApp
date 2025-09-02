import requests
from .env_data import api_key_geo
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QThread

def get_coords_by_city(city_name: str, country_name):
    response = requests.get(f'https://api.geoapify.com/v1/geocode/search?text={city_name}, {country_name}&format=json&apiKey={api_key_geo}')
    if response.status_code == 200:
        data = response.json() 
        if data["results"]:
            return[data["results"][0]["lon"], data["results"][0]["lat"]]
    return []

def get_city_name_by_coords(lon, lat):
    response = requests.get(f'https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&format=json&apiKey={api_key_geo}')
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data["results"]:
            print(data["results"][0].get("city"))
            return data["results"][0].get("city")


class MapLoader(QThread):
    finished = pyqtSignal(object)

    def __init__(self, lon, lat):
        super().__init__()
        self.lon = lon
        self.lat = lat

    def run(self):
        # Завантажуємо карту у фоновому потоці
        response = requests.get(f"https://maps.geoapify.com/v1/staticmap?style=osm-bright&width=400&height=300&center=lonlat:{self.lon},{self.lat}&zoom=14&apiKey={api_key_geo}")
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            pixmap = pixmap.scaled(289, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.finished.emit({"pixmap": pixmap})
            return
        self.finished.emit({"pixmap": None})
        

def prepare_coords(coords: str):
    coords = coords.replace(',', '.')
    coords = coords.split('. ')
    return coords if len(coords) > 1 else None