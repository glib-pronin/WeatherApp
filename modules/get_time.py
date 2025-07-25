from datetime import timedelta, datetime
def get_local_time(timestamp, timezone):
    local_time = datetime.utcfromtimestamp(timestamp)+timedelta(seconds=timezone)
    return local_time.strftime('%H:%M')