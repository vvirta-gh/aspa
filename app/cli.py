from loguru import logger
import click
from app.commands.time import get_current_time
from app.utils.display import display_datetime


@click.group()
def cli():
    """ASPA - Personal home application collection"""
    pass


@cli.command()
def time():
    """Show current time"""
    result = get_current_time()
    display_datetime(result)


def main():
    """Main entry point for the CLI"""
    logger.info("Aspa CLI started")
    cli()


if __name__ == "__main__":
    main()
