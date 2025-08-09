import json
from .get_json_data import config_path, get_json

def change_file(filename, key, value):
    data = get_json(filename)
    data[key] = value
    with open(f"{config_path}/{filename}", mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)