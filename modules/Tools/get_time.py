from datetime import datetime, timedelta

def get_local_time(timezone):
    local_time = datetime.utcnow() + timedelta(seconds=timezone)
    return local_time.strftime('%H:%M')
