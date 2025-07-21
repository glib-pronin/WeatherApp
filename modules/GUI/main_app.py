import customtkinter as ctk
from PIL import Image
from ..get_weather_data import get_weather
import os, json

assets_path = os.path.abspath(__file__+"/../../../assets")

def printframe(event):
    print("Frame")

def print_lbl(event):
    print("Label")

class App(ctk.CTk):
    def __init__(self, width, height, name):
        super().__init__(fg_color="red")
        self.title(name)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width-width)//2
        y = (screen_height-height)//2
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False, False)

        # Основна панель
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.pack(fill="both", expand=True)
        self.main_panel.columnconfigure(1, weight=1)

        self.bg_image = ctk.CTkImage(Image.open(f"{assets_path}/images/background.png"), size=(width, height))
        self.bg_label = ctk.CTkLabel(self.main_panel, image=self.bg_image, text="", fg_color="transparent")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Вміст
        self.position_frame=ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.position_frame.grid(row=0, column=0, pady=(10, 0), padx=20)
        self.position_img = ctk.CTkImage(Image.open(f"{assets_path}/images/vector.png"), size=(16, 16))
        self.icon_label = ctk.CTkLabel(self.position_frame, image=self.position_img, text="")
        self.icon_label.grid(row=0, column=0)
        self.position_label = ctk.CTkLabel(self.position_frame, text="Поточна позиція", font=("Roboto", 14))
        self.position_label.grid(row=0, column=1, padx=10)

        self.refresh_img = ctk.CTkImage(Image.open(f"{assets_path}/images/refresh.png"), size=(50, 50))
        self.refresh_label = ctk.CTkLabel(self.main_panel, image=self.refresh_img, text="", fg_color="#FFDF56")
        self.refresh_label.grid(row=0, column=1, sticky="e", padx=20, pady=20)
        self.refresh_label.bind("<Button-1>", lambda event: self.get_data(event, "Дніпро"))
        self.refresh_label.configure(cursor="hand2")

        self.city_label = ctk.CTkLabel(self.main_panel, text="Dnipro", font=("Roboto", 34, "bold"), fg_color="transparent")
        self.city_label.grid(row=1, column=0, sticky="w", pady=20, padx=20)

        self.temperature_frame=ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.temperature_frame.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="w")
        self.weather_img = ctk.CTkImage(Image.open(f"{assets_path}/icons/02n.png"), size=(64, 64))
        self.weather_img_label = ctk.CTkLabel(self.temperature_frame, image=self.weather_img, text="")
        self.weather_img_label.grid(row=0, column=0, sticky="w")

        self.temperature_label = ctk.CTkLabel(self.temperature_frame, text="11", font=("Roboto", 44, "bold"))
        self.temperature_label.grid(row=0, column=1, sticky="ws")

        self.weather_label = ctk.CTkLabel(self.main_panel, text="Cloudy", font=("Roboto", 18))
        self.weather_label.grid(row=3, column=0, sticky="w", pady=10, padx=20)
        
        self.temperature_range_label = ctk.CTkLabel(self.main_panel, text="Max: 20, min: 10", font=("Roboto", 18))
        self.temperature_range_label.grid(row=4, column=0, sticky="w", padx=20)

        self.get_data("Дніпро")

    def get_data(self, event=None, city_name="Дніпро"):
        data = get_weather(city_name)
        print(data)
        if not data:
            print("Помилка отримання даних з API")
            return
        self.city_label.configure(text=city_name)
        self.temperature_label.configure(text=f"{round(data['main']['temp'])}°")
        self.weather_img = ctk.CTkImage(Image.open(f"{assets_path}/icons/{data['weather'][0]['icon']}.png"), size=(64, 64))
        self.weather_img_label.configure(image=self.weather_img)
        self.weather_label.configure(text=data["weather"][0]["description"].capitalize())
        self.temperature_range_label.configure(text=f"Макс.:{round(data['main']['temp_max'])}°, мін.:{round(data['main']['temp_min'])}°")

app = App(350, 350, "WeatherApp")
