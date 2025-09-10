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
    

    # @patch.object(PomodoroTimer, 'is_input_available')
    # @patch.object(PomodoroTimer, 'get_input')
    # def test_run_timer_with_user_input(self, mock_get_input, mock_is_input_available):
    #     """Test that run_timer sets running state correctly when user input is available"""
    #     timer = PomodoroTimer()
    #     timer.run_timer(32, "Test", resume_seconds=1) # 1 sekunti resume_seconds:lla

        
        @patch('app.models.pomodoro.time.sleep')
        @patch('app.models.pomodoro.Confirm.ask', return_value=True)
        @patch.object(PomodoroTimer, 'get_input', return_value='\n')
        @patch.object(PomodoroTimer, 'is_input_available', return_value=True)
        def test_run_timer_enter_triggers_pause_break(self, mock_is_input_available, mock_get_input, mock_confirm_ask, mock_sleep):
            """When Enter is pressed during Work, and user confirms pause, _start_pause_break is called with current state."""
            timer = PomodoroTimer()
            # No-op prints and sleep for speed/stability
            mock_sleep.side_effect = lambda *_: None
            # Spy on _start_pause_break to assert it is called with expected args
            with patch.object(PomodoroTimer, '_start_pause_break', return_value='PAUSED') as mock_pause:
                result = timer.run_timer(minutes=1, session_type="Work", resume_seconds=3)
            assert result == 'PAUSED'
            mock_pause.assert_called_once_with(1, 3, "Work")
        
        @patch('app.models.pomodoro.time.sleep')
        @patch('app.models.pomodoro.Confirm.ask', return_value=False)
        @patch.object(PomodoroTimer, 'get_input', return_value='\n')
        def test_run_timer_enter_but_decline_pause_continues(self, mock_get_input, mock_confirm_ask, mock_sleep, monkeypatch):
            """If Enter is pressed but user declines pause, timer continues and completes."""
            timer = PomodoroTimer()
            # Provide input availability only on first check, then False
            calls = {'n': 0}
            def available_once():
                calls['n'] += 1
                return calls['n'] == 1
            monkeypatch.setattr(PomodoroTimer, 'is_input_available', staticmethod(available_once))
            # Prevent delays
            mock_sleep.side_effect = lambda *_: None
            # Ensure we don't accidentally call pause
            with patch.object(PomodoroTimer, '_start_pause_break') as mock_pause:
                result = timer.run_timer(minutes=1, session_type="Work", resume_seconds=1)
            assert result is True
            mock_pause.assert_not_called()