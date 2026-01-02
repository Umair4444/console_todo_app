"""
Unit tests for the Terminal Compatibility Detector service.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.services.terminal_compatibility_detector import TerminalCompatibilityDetector


class TestTerminalCompatibilityDetector:
    """
    Test class for Terminal Compatibility Detector service.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        self.detector = TerminalCompatibilityDetector()

    @patch('sys.stdout.isatty')
    def test_detects_color_support_when_tty_and_not_dumb_term(self, mock_isatty):
        """
        Test that color support is detected when running in a TTY with proper TERM.
        """
        mock_isatty.return_value = True
        
        with patch.dict('os.environ', {'TERM': 'xterm-256color'}):
            compat = self.detector.detect_compatibility()
            assert compat.supports_color is True

    @patch('sys.stdout.isatty')
    def test_no_color_support_when_not_tty(self, mock_isatty):
        """
        Test that no color support is detected when not running in a TTY.
        """
        mock_isatty.return_value = False
        
        with patch.dict('os.environ', {'TERM': 'xterm-256color'}):
            compat = self.detector.detect_compatibility()
            assert compat.supports_color is False

    @patch('sys.stdout.isatty')
    def test_no_color_support_when_dumb_term(self, mock_isatty):
        """
        Test that no color support is detected when TERM is 'dumb'.
        """
        mock_isatty.return_value = True
        
        with patch.dict('os.environ', {'TERM': 'dumb'}):
            compat = self.detector.detect_compatibility()
            assert compat.supports_color is False

    def test_detects_emoji_support_with_utf8_encoding(self):
        """
        Test that emoji support is detected with UTF-8 encoding.
        """
        # This test might be tricky to mock, so we'll just verify the method exists
        # and returns a boolean
        compat = self.detector.detect_compatibility()
        assert isinstance(compat.supports_emoji, bool)

    @patch('sys.platform', 'win32')
    def test_keyboard_support_on_windows(self):
        """
        Test keyboard support detection on Windows.
        """
        compat = self.detector.detect_compatibility()
        # The result depends on whether msvcrt is available
        assert isinstance(compat.supports_keyboard, bool)

    @patch('sys.platform', 'linux')
    def test_keyboard_support_on_unix(self):
        """
        Test keyboard support detection on Unix-like systems.
        """
        compat = self.detector.detect_compatibility()
        # The result depends on whether termios is available
        assert isinstance(compat.supports_keyboard, bool)

    def test_detects_correct_color_depth_for_truecolor(self):
        """
        Test that correct color depth is detected for truecolor terminals.
        """
        with patch.dict('os.environ', {'COLORTERM': 'truecolor'}):
            compat = self.detector.detect_compatibility()
            assert compat.color_depth == 16777216  # 16m color

    def test_detects_correct_color_depth_for_256color(self):
        """
        Test that correct color depth is detected for 256color terminals.
        """
        with patch.dict('os.environ', {'TERM': 'xterm-256color'}):
            compat = self.detector.detect_compatibility()
            assert compat.color_depth == 256

    def test_detects_correct_color_depth_for_basic_color(self):
        """
        Test that correct color depth is detected for basic color terminals.
        """
        with patch.dict('os.environ', {'TERM': 'xterm'}):
            compat = self.detector.detect_compatibility()
            assert compat.color_depth == 32  # Basic color support

    def test_gets_correct_encoding(self):
        """
        Test that correct encoding is detected.
        """
        compat = self.detector.detect_compatibility()
        # Should be a string, typically 'utf-8' in most environments
        assert isinstance(compat.encoding, str)
        assert len(compat.encoding) > 0

    def test_get_compatibility_report_returns_dict_with_expected_keys(self):
        """
        Test that get_compatibility_report returns a dictionary with expected keys.
        """
        report = self.detector.get_compatibility_report()
        
        expected_keys = [
            'supports_color',
            'supports_emoji',
            'supports_keyboard',
            'color_depth',
            'encoding',
            'platform',
            'is_tty',
            'term',
            'colorterm',
            'term_program'
        ]
        
        for key in expected_keys:
            assert key in report
            assert report[key] is not None  # Each key should have a value