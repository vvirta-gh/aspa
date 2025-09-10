from app.models.pomodoro import PomodoroTimer
from unittest.mock import patch


class TestPomodoroTimer:
    def test_initialization(self):
        """Test that PomodoroTimer initializes correctly"""
        timer = PomodoroTimer()
        assert timer is not None
        assert timer.settings is not None
        assert timer.stats is not None
        assert timer.running is False
        assert timer.pause_state is None
        assert timer.console is not None

    def test_default_settings(self):
        """Test that default settings are correct"""
        timer = PomodoroTimer()
        
        # Tarkista oletusasetukset
        assert timer.settings['work_duration'] == 25
        assert timer.settings['short_break'] == 5
        assert timer.settings['long_break'] == 15
        assert timer.settings['long_break_interval'] == 4

    def test_default_stats(self):
        """Test that default stats are zero"""
        timer = PomodoroTimer()
        
        # Tarkista että tilastot alustuvat nollilla
        assert timer.stats['total_sessions'] == 0
        assert timer.stats['pomodoros_today'] == 0
        assert timer.stats['sessions_today'] == 0
        assert timer.stats['total_worktime'] == 0

    
    @patch('app.models.pomodoro.time.sleep')  # Mock time.sleep niin ettei odota oikeasti
    @patch.object(PomodoroTimer, 'is_input_available')  # Mock input-lukeminen
    @patch.object(PomodoroTimer, 'get_input')  # Mock input-lukeminen
    def test_run_timer_starts_running(self, mock_get_input, mock_is_input_available, mock_sleep):
        """Test that run_timer sets running state correctly"""
        timer = PomodoroTimer()
        
        # Mock input-metodit niin että ne eivät yritä lukea oikeaa syötettä
        mock_is_input_available.return_value = False  # Ei syötettä saatavilla
        mock_get_input.return_value = ''  # Tyhjä syöte
        
        # Ajetaan timer 1 sekunnin ajan (ei 1 minuutti, koska testit)
        timer.run_timer(1, "Test", resume_seconds=1)  # 1 sekunti resume_seconds:lla
        
        # Tarkista että running-tila on ausetettu
        assert timer.running is True