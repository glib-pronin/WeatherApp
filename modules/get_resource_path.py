import os, sys

def get_path(relative_path):
    try:
        return os.path.abspath(sys._MEIPASS+f"/{relative_path}")
    except:
        return os.path.abspath(__file__+f"/../../{relative_path}")
