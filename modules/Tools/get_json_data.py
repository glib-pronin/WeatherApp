import json, os

config_path = os.path.abspath(__file__ + "/../../../static/configs")


def get_json(filename: str):
    with open(f"{config_path}/{filename}", encoding="utf-8") as f:
        return json.load(f)
