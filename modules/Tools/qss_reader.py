from .static_loader import get_image_path
import os


static_path = os.path.abspath(__file__ +"/../../../static")

def get_image_path(relative_path: str):
    return f"{static_path}/{relative_path}"

qss_path = os.path.abspath(__file__+"/../../../static/qss")

def read_qss_file(filename: str):
    with open(f"{qss_path}/{filename}") as f:
        file = f.read()
        return file.replace("url_for_replacement", get_image_path("images/grid.png").replace('\\', '/'))