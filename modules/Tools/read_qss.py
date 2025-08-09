import os

qss_path = os.path.abspath(__file__+"/../../../static/qss")

def read_qss_file(filename: str):
    with open(f"{qss_path}/{filename}") as f:
        return f.read()
    
