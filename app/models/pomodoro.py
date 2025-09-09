import time
import signal
import sys
import platform
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
        self.pause_state = None
    

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
        self.console.print("[dim]Press Enter during work to take a break, Ctrl+C to cancel[/dim]")

        if self.run_timer(self.settings['work_duration'], "Work"):
            self.stats['pomodoros_today'] += 1
            self.stats['sessions_today'] += 1 
            self.stats['total_worktime'] += self.settings['work_duration']

            # Ask if user wants to take a break
            if Confirm.ask("Would you like to take a break?"):
                break_duration = self.settings['long_break'] if self.stats['pomodoros_today'] % self.settings['long_break_interval'] == 0 else self.settings['short_break']
                break_type = "Long" if break_duration == self.settings['long_break'] else "Short"

                self.console.print(f"\n[green]☕ Taking {break_duration}min {break_type} break...[/green]")
                self.run_timer(break_duration, f"{break_type} Break")
    
    def run_timer(self, minutes, session_type, resume_seconds=None):
        """Run timer for given duration with non-blocking input support"""
        self.running = True
        
        # Jos resume_seconds on annettu, käytä sitä, muuten aloita alusta
        if resume_seconds is not None:
            seconds = resume_seconds
        else:
            seconds = minutes * 60

        try:
            while seconds > 0 and self.running:
                mins, secs = divmod(seconds, 60)
                # Show dynamic session label instead of literal "[session_type]"
                self.console.print(
                    f"\t{mins:02d}:{secs:02d}", 
                    end="", 
                    style="bold")
                
                # Check for non-blocking input (cross-platform)
                if self.is_input_available():
                    input_data = self.get_input()
                    if input_data == '\r' or input_data == '\n':  # Enter key pressed
                        if session_type == "Work" and Confirm.ask("\nTake a pause?"):
                            return self._start_pause_break(minutes, seconds, session_type)
                        else:
                            self.console.print(f"\n[yellow]Continuing {session_type.lower()}...[/yellow]")
                
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
    
    def _start_break(self):
        """Start a break session"""
        break_duration = self.settings['long_break'] if self.stats['pomodoros_today'] % self.settings['long_break_interval'] == 0 else self.settings['short_break']
        break_type = "Long" if break_duration == self.settings['long_break'] else "Short"
        
        self.console.print(f"\n[green]☕ Starting {break_duration}min {break_type} break...[/green]")
        return self.run_timer(break_duration, f"{break_type} Break")


    def _start_pause_break(self, minutes, seconds, session_type):
        """Start a pause break"""
        # 1. Tallennetaan tilanne ennen taukoa
        self.pause_state = {
            'minutes': minutes,           # Alkuperäinen kesto
            'seconds': seconds,           # Jäljellä olevat sekunnit
            'session_type': session_type, # "Work", "Short Break" tai "Long Break"
        }
        
        # 2. Näytetään taukoilmoitus
        mins, secs = divmod(seconds, 60)
        self.console.print(f"\n[yellow]⏸️  {session_type} paused[/yellow]")
        self.console.print(f"Time left: {mins:02d}:{secs:02d}")
        
        # 3. Odota Enteria palatakseen
        self.console.print("[dim]Press Enter to resume...[/dim]")
        
        # 4. Odota Enter-painallusta
        while True:
            if self.is_input_available():
                input_data = self.get_input()
                if input_data == '\r' or input_data == '\n':  # Enter pressed
                    self.console.print(f"\n[green]▶️  Resuming {session_type}...[/green]")
                    break
            time.sleep(0.1)
        
        # 5. Palauta timer samaan kohtaan
        return self.run_timer(minutes, session_type, resume_seconds=seconds)



    def is_input_available(self):
        """Check if input is available (cross-platform)"""
        os_name = platform.system()  # "Windows", "Darwin" (MacOS), "Linux"
        if os_name == "Windows":
            return self._is_input_available_windows()
        elif os_name == "Linux":
            return self._is_input_available_unix()
        elif os_name == "Darwin":
            return self._is_input_available_unix()  # MacOS uses Unix-like input availability check
        else:
            self.console.print(f"[red]❌ Unsupported operating system: {os_name}[/red]")
            return False

    def _is_input_available_windows(self):
        """Check if input is available on Windows"""
        import msvcrt
        return msvcrt.kbhit()  # Returns True if a key has been pressed since last check (kbhit = keyboard hit)

    def _is_input_available_unix(self):
        """Check if input is available on Unix/Linux/MacOS"""
        import select
        # select.select() is a function that waits for input to be available
        # 1. [sys.stdin] listen to the standard input stream (keyboard)
        # 2. [] does not listen to the standard output stream (screen)
        # 3. [] does not listen to the standard error stream (console)
        # 4. 0 is the timeout in seconds (0 = non-blocking)
        # 5. [0] returns the list of streams that are ready to be read
        return sys.stdin in select.select([sys.stdin], [], [], 0)[0]  # Returns True if input is available, False otherwise


    def get_input(self):
        """Get input when available (cross-platform)"""
        os_name = platform.system()
        if os_name == "Windows":
            import msvcrt
            return msvcrt.getch().decode('utf-8')  # Read single character and decode from bytes
        else:
            # For Unix/Linux, read the line but don't strip the newline
            # so we can detect Enter key press
            return sys.stdin.readline()  # Don't strip - keep the \n character



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
