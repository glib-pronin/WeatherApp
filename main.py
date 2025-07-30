from modules import app

def main():
    try:
        app.exec()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()