from datetime import datetime


def get_current_time():
    """Get current time as formatted string"""
    timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def start_pomodoro():
    """Start pomodoro timer"""