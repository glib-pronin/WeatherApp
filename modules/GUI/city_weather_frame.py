import customtkinter as ctk

class CityWeatherFrame(ctk.CTkFrame):
    def __init__(self, master, name, code, time, temp, desc, tmax, tmin, width = 330, height = 110, fg_color= None, **kwargs):
        super().__init__(master=master, width=width, height=height, fg_color=fg_color, **kwargs)

        self.city_name = name
        self.icon_code = code 

        self.grid_propagate(False)
        self.columnconfigure(1, weight=1)

        self.city_name_lbl = ctk.CTkLabel(self, text=name, font=("Robot", 24, "bold"))
        self.city_name_lbl.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
        self.time = ctk.CTkLabel(self, text=time, font=("Roboto", 12, "bold"))
        self.time.grid(row=1, column=0, sticky="w", padx=(10, 0))
        self.weather_desc = ctk.CTkLabel(self, text=desc.capitalize(), font=("Roboto", 12, "bold"))
        self.weather_desc.grid(row=2, column=0, sticky="w", padx=(10, 0))
        self.temp_value = ctk.CTkLabel(self, text=f"{round(temp)}°", font=("Roboto", 44, "bold"))
        self.temp_value.grid(row=0, column=1, sticky="e", rowspan=2, padx=(0, 10), pady=(10, 0))
        self.temp_range = ctk.CTkLabel(self, text=f"Макс.:{round(tmax)}°, мін.:{round(tmin)}°", font=("Roboto", 12, "bold"))
        self.temp_range.grid(row=2, column=1, sticky="e", padx=(0, 10))
        self.line = LineFrame(self, width=330, height=2, fg_color="#C6C8C9")
        self.line.grid(row=3, column=0, columnspan=2, padx=(10, 10))

    def change_text_color(self, color):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=color)

class LineFrame(ctk.CTkFrame):
    def __init__(self, master, width = 330, height = 1, fg_color = None, **kwargs):
        super().__init__(master=master, width=width, height=height, fg_color=fg_color, **kwargs)


        