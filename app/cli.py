from loguru import logger
import click
from app.commands.time import get_current_time
from app.models.pomodoro import PomodoroTimer
from app.utils.display import display_datetime


@click.group()
def cli():
    """ASPA - Personal home application collection"""
    pass


@cli.group()
def timer():
    """Time-related commands"""
    pass
 

@timer.command()
def now():
    """Show current time"""
    result = get_current_time()
    display_datetime(result)


@timer.command()
def pomo():
    """Start pomodoro timer console"""
    logger.info("Starting pomodoro timer console...")
    timer = PomodoroTimer()
    timer.show_main_menu()


def main():
    """Main entry point for the CLI"""
    logger.info("Aspa CLI started")
    cli()


if __name__ == "__main__":
    main()
