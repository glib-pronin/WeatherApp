import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from ..get_weather_data import get_weather
import os


assets_path = os.path.abspath(__file__+"/../../../assets")

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
        # self.overrideredirect(True)

        # Canvas
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.show_main_window) 
        self.update()

        self.bg_image = ImageTk.PhotoImage(Image.open(f"{assets_path}/images/background.png").resize((self.canvas.winfo_width(), self.canvas.winfo_height())))
        self.vector_icon = ImageTk.PhotoImage(Image.open(f"{assets_path}/images/vector.png").resize((20, 20)))
        self.refresh_icon = ImageTk.PhotoImage(Image.open(f"{assets_path}/images/refresh.png").resize((62, 62)))
        self.weather_icon = ImageTk.PhotoImage(Image.open(f"{assets_path}/icons/04d.png").resize((150, 150)))


        # Фонове зображення
        self.canvas.create_image(0, 0,  anchor="nw", image=self.bg_image)
        print("Image size:", self.bg_image.width(), self.bg_image.height())
        print("Canvas size:", self.canvas.winfo_width(), self.canvas.winfo_height())

        # Поточна позиція (іконка + текст)
        self.canvas.create_image(20, 40, anchor="nw", image=self.vector_icon)
        self.canvas.create_text(50, 40, text="Поточна позиція", font=("Roboto", 14, "bold"), anchor="nw", fill="white")

        # Refresh-кнопка
        self.refresh_button = self.canvas.create_image(350, 20, anchor="nw", image=self.refresh_icon)
        self.canvas.tag_bind(self.refresh_button, "<Button-1>", lambda event: self.get_data(event, "Дніпро"))
        self.canvas.tag_bind(self.refresh_button, "<Enter>", lambda event: self.change_cursor(event, True))
        self.canvas.tag_bind(self.refresh_button, "<Leave>", lambda event: self.change_cursor(event, False))

        # Назва міста
        self.city_label = self.canvas.create_text(20, 90, text="Дніпро", font=("Roboto", 34, "bold"), anchor="nw", fill="white")

        # Температура + іконка
        self.temp_icon = self.canvas.create_image(-30, 145, anchor="nw", image=self.weather_icon)
        self.temp_label = self.canvas.create_text(110, 175, text="28°", font=("Roboto", 50, "bold"), anchor="nw", fill="white")

        # Стан погоди
        self.weather_desc = self.canvas.create_text(20, 280, text="Хмарно", font=("Roboto", 18, "bold"), anchor="nw", fill="white")

        # Діапазон температур
        self.temp_range = self.canvas.create_text(20, 330, text="Макс.:28°, мін.:28°", font=("Roboto", 18), anchor="nw", fill="white")

        self.get_data("Дніпро")
    
    def get_data(self, event=None, city_name="Дніпро"):
        data = get_weather(city_name)
        print(data)
        if not data:
            print("Помилка отримання даних з API")
            return
        icon = App.check_icon(data['weather'][0]['icon'])
        self.canvas.itemconfig(self.city_label, text=city_name)
        self.canvas.itemconfig(self.temp_label, text=f"{round(data['main']['temp'])}°")
        self.canvas.itemconfig(self.weather_desc, text=data["weather"][0]["description"].capitalize())
        self.canvas.itemconfig(self.temp_range,text=f"Макс.:{round(data['main']['temp_max'])}°, мін.:{round(data['main']['temp_min'])}°")
        self.weather_icon = ImageTk.PhotoImage(Image.open(f"{assets_path}/icons/{icon}.png").resize((150, 150)))
        self.canvas.itemconfig(self.temp_icon, image=self.weather_icon)

    def change_cursor(self, event, hand):
        self.canvas.config(cursor="hand2") if hand else self.canvas.config(cursor="")

    def show_main_window(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if self.refresh_button in items:
            print("Клік по кнопці оновлення, не відкриваємо модальне вікно")
            return
        self.main_window = ctk.CTkToplevel(width=1200, height=800)
        self.main_window.grab_set()

    @staticmethod
    def check_icon(icon=None):
        icons = [file.replace(".png", "") for file in os.listdir(f"{assets_path}/icons")]
        if icon in icons:
            return icon
        else:
            return "04d"

app = App(350, 350, "WeatherApp")
    