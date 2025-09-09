import time
import signal
import sys
from datetime import datetime, timedelta
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from loguru import logger


class PomodoroTimer:
    def __init__(self):
        self.console = Console()
        self.settings = {
            'work_duration': 25,    # minutes
            'short_break': 5,       # minutes
            'long_break': 15,       # minutes
            'long_break_interval': 4, 
        }
        self.stats = {
            'total_sessions': 0,
            'pomodoros_today': 0,
            'sessions_today': 0,
            'total_worktime': 0,    
        }
        self.running = False
    

    def show_main_menu(self):
        """Show main menu"""
        while True:
            self.console.clear()
            self.console.print(Panel.fit(
                "[bold dark_blue]🍅 Pomodoro Timer[/bold dark_blue]\n"
                f"Today: {self.stats['pomodoros_today']} pomodoros\n"
                f"Sessions: {self.stats['sessions_today']}\n"
                f"Total worktime: {self.stats['total_worktime']} minutes\n"
                "\n"
                "[bold dark_blue]Options:[/bold dark_blue]\n"
                "1. Start a new session\n"
                "2. View settings\n"
                "3. View stats\n"
                "4. Exit\n",
                title="Main Menu",
                border_style="dark_blue"
            ))
            
            choice = Prompt.ask(
                "Choose an option:",
                choices=["1", "2", "3", "4"],
                default="1"
            )

            if choice == "1":
                self.start_session()
            elif choice == "2":
                self.configure_settings()
            elif choice == "3":
                self.view_stats()
            elif choice == "4":
                break
            time.sleep(0.1)
    
    def start_session(self):
        """Start a new session"""
        self.console.print(f"\n[green]🍅 Starting {self.settings['work_duration']}min work session...[/green]")

        if self.run_timer(self.settings['work_duration'], "Work"):
            self.stats['pomodoros_today'] += 1
            self.stats['sessions_today'] += 1 
            self.stats['total_worktime'] += self.settings['work_duration']

            # Ask if user wants to take a break
            if Confirm.ask("Would you like to take a break?"):
                break_duration = self.settings['long_break'] if self.stats['pomodoros_today'] % self.settings['long_break_interval'] == 0 else self.settings['short_break']
                break_type = "Long" if break_duration == self.settings['long_break'] else "Short"

                self.console.print(f"\n[green]🍅 Taking {break_duration}min {break_type} break...[/green]")
                self.run_timer(break_duration, f"{break_type} Break")
    
    def run_timer(self, minutes, session_type):
        """Run timer for given duration"""
        self.running = True
        seconds = minutes * 60

        try:
            while seconds > 0 and self.running:
                mins, secs = divmod(seconds, 60)
                self.console.print(f"\r[session_type]: {mins:02d}:{secs:02d}", end="", style="bold")
                time.sleep(1)
                seconds -= 1
                
            if self.running:
                self.console.print(f"\n[green]✅ {session_type} completed![/green]")
                return True
            else:
                return False
                
        except KeyboardInterrupt:
            self.running = False
            self.console.print(f"\n[yellow]⏸️  {session_type} cancelled[/yellow]")
            return False

    def configure_settings(self):
        """Configure pomodoro settings"""
        self.console.print("\n[bold]⚙️  Configure Settings[/bold]")
        
        work = Prompt.ask("Work duration (minutes)", default=str(self.settings['work_duration']))
        short_break = Prompt.ask("Short break (minutes)", default=str(self.settings['short_break']))
        long_break = Prompt.ask("Long break (minutes)", default=str(self.settings['long_break']))
        interval = Prompt.ask("Long break interval", default=str(self.settings['long_break_interval']))
        
        try:
            self.settings['work_duration'] = int(work)
            self.settings['short_break'] = int(short_break)
            self.settings['long_break'] = int(long_break)
            self.settings['long_break_interval'] = int(interval)
            self.console.print("[green]✅ Settings updated![/green]")
        except ValueError:
            self.console.print("[red]❌ Invalid input![/red]")
            
    def view_stats(self):
        """Show pomodoro statistics"""
        table = Table(title="📊 Pomodoro Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Today's Pomodoros", str(self.stats['pomodoros_today']))
        table.add_row("Sessions Today", str(self.stats['sessions_today']))
        table.add_row("Total Work Time", f"{self.stats['total_worktime']} minutes")
        
        if self.stats['sessions_today'] > 0:
            avg_work = self.stats['total_worktime'] / self.stats['sessions_today']
            table.add_row("Avg Work per Session", f"{avg_work:.1f} minutes")
        
        self.console.print(table)
        Prompt.ask("\nPress Enter to continue")