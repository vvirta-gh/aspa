from rich.console import Console
import click
from app.cli import cli
from app.commands.time import time_command
console = Console()

@cli.command()
def display_time():
    """Display current time with consistent styling"""
    console.print(
        f"[dark_blue]Date:[/dark_blue] [bold blue]{datetime}[/bold blue]"
    )