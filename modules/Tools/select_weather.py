from .get_json_data import get_json

weather_types = get_json("weather_types.json")

def select_weather_type(img_code):
        for type, codes in weather_types.items():
            if img_code in codes:
                return type
        return "weatherWidget"