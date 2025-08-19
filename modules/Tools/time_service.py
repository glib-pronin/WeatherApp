from datetime import datetime, timedelta

# Словник з перекладом днів тижня
translated_date_of_week = {
    "Monday": "Понеділок",
    "Tuesday": "Вівторок",
    "Wednesday": "Середа",
    "Thursday": "Четвер",
    "Friday": "П'ятниця",
    "Saturday": "Субота",
    "Sunday": "Неділя"
}

def get_local_date_time(timezone: int):
    local_time = datetime.utcnow() + timedelta(seconds=timezone)
    return {
        "local_time": local_time.strftime("%H:%M"),
        "local_day_of_week": translated_date_of_week[local_time.strftime("%A")],
        "local_date": local_time.strftime("%d.%m.%Y")
        }

def calc_time(time: str, timezone: int):
    time_obj = datetime.strptime(time, "%H:%M")
    return (time_obj + timedelta(seconds=timezone)).strftime("%H:%M")
