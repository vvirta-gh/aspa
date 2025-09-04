from datetime import datetime


def time_command():
    timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
