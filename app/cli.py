from loguru import logger
import click
from app.commands.time import time_command
from rich.console import Console


@click.group()
def cli():
    """ASPA - Personal home application collection"""
    pass


@cli.command()
def time():
    """Show current time"""
    result = time_command()
    datetime = result.split(" ")[0]
    time = result.split(" ")[1]
    Console().print(
        f"[dark_blue]Date:[/dark_blue] [bold blue]{datetime}[/bold blue]"
    )
    Console().print(
        f"[dark_blue]Time:[/dark_blue] [bold blue]{time}[/bold blue]"
    )


def main():
    """Main entry point for the CLI"""
    logger.info("Aspa CLI started")
    cli()


if __name__ == "__main__":
    main()
