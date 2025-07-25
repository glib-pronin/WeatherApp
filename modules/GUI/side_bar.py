import customtkinter as ctk
from PIL import Image
from ..get_resource_path import get_path
from ..get_weather_data import get_weather
from ..get_time import get_local_time
from ..get_json_data import get_json
from .city_weather_frame import CityWeatherFrame


class SideBar(ctk.CTkFrame):
    def __init__(self, master, width, height, bind_children, switch_theme_callback, **kwargs):
        super().__init__(master=master, width=width, height=height, fg_color="#485c64", **kwargs)
        self.bind_children = bind_children
        self.switch_theme_callback = switch_theme_callback
        self.grid_propagate(False)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.light_img = ctk.CTkImage(Image.open(get_path("assets/images/light.png")), size=(18, 18))
        self.dark_img = ctk.CTkImage(Image.open(get_path("assets/images/dark.png")), size=(18, 18))
        self.switch_theme_btn = ctk.CTkFrame(self, width=52, height=24, fg_color="white", corner_radius=30)
        self.switch_theme_btn.grid(row=0, column=1, sticky="ne", padx=20, pady=20)
        self.switch_theme_btn.configure(cursor="hand2")
        self.switch_theme_btn.pack_propagate(False)
        self.switch_theme_lbl = ctk.CTkLabel(self.switch_theme_btn, height=16, image=self.dark_img, text="")
        self.switch_theme_lbl.pack(side="right", padx=(0, 5))

        self.bind_children(self.switch_theme_btn, None, self.switch_theme_callback, "<Button-1>")

        self.cities_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color="#283439")
        self.cities_frame.grid(row=1, column=0, columnspan=2, sticky="wens", padx=(0, 4))

        self.cities_names = None
        self.cities_list = []

        self.init_cities("cities")
        if self.cities_list:
            self.selected_city = self.cities_list[0] if self.cities_list else None
            self.selected_city.configure(fg_color="#2a373c")

    def apply_theme(self, city_frame=None, change_theme=True, theme_dict=None):
        if city_frame:
            self.selected_city.configure(fg_color="#485c64")
            city_frame.configure(fg_color="#2a373c")
            self.selected_city = city_frame
        self.switch_theme_btn.configure(fg_color=theme_dict["switch_fg"])
        lbl_image=getattr(self, theme_dict["switch_image"])
        self.switch_theme_lbl.configure(image=lbl_image)
        padx_tuple = tuple(theme_dict["switch_pack"]["padx"])
        self.switch_theme_lbl.pack(side=theme_dict["switch_pack"]["side"], padx=padx_tuple)
        self.configure(fg_color=theme_dict["frame_fg"])
        self.cities_frame.configure(fg_color=theme_dict["frame_fg"])

    def add_city_frame(self, name, code, time, temp, desc, tmax, tmin):
        city = CityWeatherFrame(self.cities_frame, name, code, time, temp, desc, tmax, tmin, 330, 110, "#485c64")
        city.pack(pady=(0, 20))
        self.bind_children(city, None, lambda event, city=city: self.switch_theme_callback(event, city_frame=city, change_theme=False), "<Button-1>")
        self.cities_list.append(city)

    def init_cities(self, filename):
        self.cities_names = get_json("cities")["cities"]
        for city in self.cities_names:
            data = get_weather(city)
            if not data:
                continue
            local_time = get_local_time(timestamp=data["dt"], timezone=data["timezone"])
            self.add_city_frame(
                city, code=data['weather'][0]['icon'], 
                time=local_time, temp=data['main']['temp'], desc=data["weather"][0]["description"], 
                tmax=data['main']['temp_max'], tmin=data['main']['temp_min']
                )
            

