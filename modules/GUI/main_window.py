import customtkinter as ctk
from .side_bar import SideBar
from ..get_json_data import get_json

class MainWindow(ctk.CTkToplevel):
    def __init__(self, width, height, bind_children, fg_color = None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width-width)//2
        y = (screen_height-height)//2
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False, False)

        self.theme = "dark"
        self.theme_dict = get_json("themes")

        self.side_bar = SideBar(self, 370, height, bind_children, self.switch_theme)
        self.side_bar.pack(side="left", fill="y")

    def switch_theme(self, event, city_frame=None, change_theme=True):
        self.theme = self.theme_dict[self.theme]["next_theme"] if change_theme else self.theme
        theme = self.theme_dict[self.theme]
        self.side_bar.apply_theme(city_frame, change_theme, theme)