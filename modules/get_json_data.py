import json 
from .get_resource_path import get_path

config_path = get_path("config")

def get_json(filename_without_ext):
    with open(f"{config_path}/{filename_without_ext}.json", encoding="utf-8") as f:
        data = json.load(f)
        return data
