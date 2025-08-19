import os

static_path = os.path.abspath(__file__ +"/../../../static")

def get_image_path(relative_path: str):
    return f"{static_path}/{relative_path}"