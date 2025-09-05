from rich.console import Console


def display_time(timestamp):
    """Display time with consistent styling"""
    Console().print(
        f"[dark_blue]Time:[/dark_blue] [bold blue]{timestamp}[/bold blue]"
    )


def display_date(date):
    """Display date with consistent styling"""
    Console().print(
        f"[dark_blue]Date:[/dark_blue] [bold blue]{date}[/bold blue]"
    )


def display_datetime(datetime_string):
    """Display both date and time from YYYY-MM-DD HH:MM:SS format"""
    date, time = datetime_string.split(" ")
    display_date(date)
    display_time(time)
