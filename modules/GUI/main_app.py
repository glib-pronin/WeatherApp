import customtkinter as ctk
from PIL import Image
from ..get_weather_data import get_weather
from ..get_resource_path import get_path
from .main_window import MainWindow
import os

assets_path = get_path("assets")

class App(ctk.CTk):
    def __init__(self, width, height, name):
        super().__init__()
        self.title(name)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width-width)//2
        y = (screen_height-height)//2
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False, False)

        # Основна панель
        self.main_panel = ctk.CTkFrame(self, fg_color="#1E90D6")
        self.main_panel.pack(fill="both", expand=True)
        self.main_panel.columnconfigure(1, weight=1)

        # Вміст
        self.position_frame=ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.position_frame.grid(row=0, column=0, pady=(10, 0), padx=20, sticky="w")
        self.position_img = ctk.CTkImage(Image.open(f"{assets_path}/images/vector.png"), size=(16, 16))
        self.icon_label = ctk.CTkLabel(self.position_frame, image=self.position_img, text="")
        self.icon_label.grid(row=0, column=0)
        self.position_label = ctk.CTkLabel(self.position_frame, text="Поточна позиція", font=("Roboto", 14))
        self.position_label.grid(row=0, column=1, padx=10)

        self.refresh_img = ctk.CTkImage(Image.open(f"{assets_path}/images/refresh.png"), size=(50, 50))
        self.refresh_label = ctk.CTkLabel(self.main_panel, image=self.refresh_img, text="", fg_color="transparent")
        self.refresh_label.grid(row=0, column=1, sticky="e", padx=20, pady=20)
        self.refresh_label.bind("<Button-1>", lambda event: self.get_data(event, "Дніпро"))
        self.refresh_label.configure(cursor="hand2")

        self.city_label = ctk.CTkLabel(self.main_panel, text="Dnipro", font=("Roboto", 34, "bold"), fg_color="transparent")
        self.city_label.grid(row=1, column=0, sticky="w", pady=0, padx=20)

        self.temperature_frame=ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.temperature_frame.grid(row=2, column=0, pady=(15, 20), padx=20, sticky="w")
        self.weather_img = ctk.CTkImage(Image.open(f"{assets_path}/icons/02d.png"), size=(64, 64))
        self.weather_img_label = ctk.CTkLabel(self.temperature_frame, image=self.weather_img, text="")
        self.weather_img_label.grid(row=0, column=0, sticky="w")

        self.temperature_label = ctk.CTkLabel(self.temperature_frame, text="Завантажується", font=("Roboto", 16, "bold"))
        self.temperature_label.grid(row=0, column=1, sticky="ws", padx=10)

        self.weather_label = ctk.CTkLabel(self.main_panel, text="Завантажується", font=("Roboto", 18, "bold"))
        self.weather_label.grid(row=3, column=0, sticky="w", pady=5, padx=20)
        
        self.temperature_range_label = ctk.CTkLabel(self.main_panel, text="Завантажується", font=("Roboto", 18))
        self.temperature_range_label.grid(row=4, column=0, sticky="w", padx=20)
        
        App.bind_all_children(self.main_panel, self.refresh_label, self.show_main_window, "<Button-1>")

        # self.get_data("Дніпро")

    def get_data(self, event=None, city_name="Дніпро"):
        data = get_weather(city_name)
        print(data)
        if not data:
            print("Помилка отримання даних з API")
            return
        App.check_icon(data['weather'][0]['icon'])
        self.city_label.configure(text=city_name)
        self.temperature_label.configure(text=f"{round(data['main']['temp'])}°", font=("Roboto", 46, "bold"))
        self.weather_img = ctk.CTkImage(Image.open(f"{assets_path}/icons/{data['weather'][0]['icon']}.png"), size=(64, 64))
        self.weather_img_label.configure(image=self.weather_img)
        self.weather_label.configure(text=data["weather"][0]["description"].capitalize())
        self.temperature_range_label.configure(text=f"Макс.:{round(data['main']['temp_max'])}°, мін.:{round(data['main']['temp_min'])}°")
    
    def show_main_window(self, event):
        self.main_window = MainWindow(width=1200, height=600, bind_children=App.bind_all_children)

    @staticmethod
    def bind_all_children(widget, exception, handler, event):
        if widget == exception:
            return
        widget.bind(event, handler)
        for child in widget.winfo_children():
            App.bind_all_children(child, exception, handler, event)

    @staticmethod
    def check_icon(icon=None):
        icons = [file.replace(".png", "") for file in os.listdir(f"{assets_path}/icons")]
        if icon in icons:
            return icon
        else:
            return "02d"
        
app = App(350, 350, "WeatherApp")
