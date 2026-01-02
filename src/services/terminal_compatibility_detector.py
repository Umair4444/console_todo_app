"""
Terminal Compatibility Detector service for detecting terminal capabilities.
"""
import sys
import os
from typing import Dict, Any
from src.models.visual_elements import TerminalCompatibility


class TerminalCompatibilityDetector:
    """
    Service class that detects terminal capabilities for visual enhancements.
    """

    def __init__(self):
        """
        Initialize the Terminal Compatibility Detector.
        """
        pass

    def detect_compatibility(self) -> TerminalCompatibility:
        """
        Detect the terminal's compatibility with various visual features.

        Returns:
            TerminalCompatibility instance with detected capabilities
        """
        supports_color = self._supports_color()
        supports_emoji = self._supports_emoji()
        supports_keyboard = self._supports_keyboard()
        color_depth = self._detect_color_depth()
        encoding = sys.stdout.encoding or 'utf-8'

        return TerminalCompatibility(
            supports_color=supports_color,
            supports_emoji=supports_emoji,
            supports_keyboard=supports_keyboard,
            color_depth=color_depth,
            encoding=encoding
        )

    def _supports_color(self) -> bool:
        """
        Check if the terminal supports color.

        Returns:
            True if color is supported, False otherwise
        """
        # Check if we're running in a terminal that supports color
        if not sys.stdout.isatty():
            return False

        # Check environment variables
        if os.environ.get('TERM') in ('dumb', 'unknown'):
            return False

        # On Windows, check for color support
        if sys.platform.startswith('win'):
            # Windows 10 version 10.0.10586 and later support ANSI colors
            import platform
            try:
                # Get Windows version
                version = platform.version().split('.')
                major = int(version[0])
                build = int(version[2]) if len(version) > 2 else 0
                
                # Windows 10 build 10586+ supports ANSI colors
                if major >= 10 and build >= 10586:
                    return True
            except (ValueError, IndexError):
                # If we can't parse the version, assume no color support
                pass

            # For older Windows versions, check if we're in a modern terminal
            return os.environ.get('WT_SESSION') is not None  # Windows Terminal

        # On Unix-like systems, check TERM
        return os.environ.get('TERM') != 'dumb'

    def _supports_emoji(self) -> bool:
        """
        Check if the terminal supports emojis.

        Returns:
            True if emoji is supported, False otherwise
        """
        # Try to print a simple emoji to test support
        try:
            # Test with a simple emoji
            test_emoji = '✅'
            # Encode and decode to check if it's supported
            test_emoji.encode(sys.stdout.encoding or 'utf-8')
            return True
        except UnicodeEncodeError:
            return False

    def _supports_keyboard(self) -> bool:
        """
        Check if the terminal supports keyboard input detection.

        Returns:
            True if keyboard input is supported, False otherwise
        """
        # Check if we're running in a terminal that supports keyboard input
        if not sys.stdout.isatty():
            return False

        # On Windows, we might need to use msvcrt
        if sys.platform.startswith('win'):
            try:
                import msvcrt
                return hasattr(msvcrt, 'getch')
            except ImportError:
                return False

        # On Unix-like systems, we can use termios
        try:
            import termios
            import tty
            return hasattr(termios, 'tcgetattr')
        except ImportError:
            return False

    def _detect_color_depth(self) -> int:
        """
        Detect the color depth of the terminal.

        Returns:
            Color depth (32 for basic, 256 for 256-color, 16m for true color)
        """
        # Check environment variables
        if os.environ.get('COLORTERM') == 'truecolor' or os.environ.get('TERM_PROGRAM') == 'iTerm.app':
            return 16777216  # 16m (true color)
        
        # Check TERM environment variable
        term = os.environ.get('TERM', '')
        if '256color' in term:
            return 256
        
        # Default to basic color support
        return 32

    def get_compatibility_report(self) -> Dict[str, Any]:
        """
        Get a detailed report of terminal compatibility.

        Returns:
            Dictionary with detailed compatibility information
        """
        compat = self.detect_compatibility()
        
        return {
            'supports_color': compat.supports_color,
            'supports_emoji': compat.supports_emoji,
            'supports_keyboard': compat.supports_keyboard,
            'color_depth': compat.color_depth,
            'encoding': compat.encoding,
            'platform': sys.platform,
            'is_tty': sys.stdout.isatty(),
            'term': os.environ.get('TERM', 'unknown'),
            'colorterm': os.environ.get('COLORTERM', 'unknown'),
            'term_program': os.environ.get('TERM_PROGRAM', 'unknown'),
        }