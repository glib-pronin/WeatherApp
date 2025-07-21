from modules import app
import customtkinter as ctk

ctk.set_appearance_mode("dark")

def main():
    try:
        app.mainloop()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

