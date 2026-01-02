"""
Utility functions for terminal capability detection and handling.
"""
import sys
import os
from typing import Tuple, Optional


def detect_color_support() -> bool:
    """
    Detect if the terminal supports color output.

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


def detect_emoji_support() -> bool:
    """
    Detect if the terminal supports emoji output.

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


def detect_keyboard_support() -> bool:
    """
    Detect if the terminal supports keyboard input detection.

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


def detect_color_depth() -> int:
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


def get_terminal_encoding() -> str:
    """
    Get the terminal's encoding.

    Returns:
        Encoding string (e.g., 'utf-8')
    """
    return sys.stdout.encoding or 'utf-8'


def get_terminal_size() -> Tuple[int, int]:
    """
    Get the terminal size (columns, rows).

    Returns:
        Tuple of (columns, rows)
    """
    try:
        # Try to get terminal size using os
        size = os.get_terminal_size()
        return size.columns, size.rows
    except OSError:
        # If that fails, return default values
        return 80, 24


def supports_visual_enhancements() -> bool:
    """
    Check if the terminal supports visual enhancements (emoji and color).

    Returns:
        True if visual enhancements are supported, False otherwise
    """
    return detect_color_support() and detect_emoji_support()


def should_use_fallback_display() -> bool:
    """
    Determine if fallback display should be used based on terminal capabilities.

    Returns:
        True if fallback display should be used, False otherwise
    """
    return not supports_visual_enhancements()


def get_compatibility_report() -> dict:
    """
    Get a detailed report of terminal compatibility.

    Returns:
        Dictionary with detailed compatibility information
    """
    return {
        'supports_color': detect_color_support(),
        'supports_emoji': detect_emoji_support(),
        'supports_keyboard': detect_keyboard_support(),
        'color_depth': detect_color_depth(),
        'encoding': get_terminal_encoding(),
        'platform': sys.platform,
        'is_tty': sys.stdout.isatty(),
        'term': os.environ.get('TERM', 'unknown'),
        'colorterm': os.environ.get('COLORTERM', 'unknown'),
        'term_program': os.environ.get('TERM_PROGRAM', 'unknown'),
        'terminal_size': get_terminal_size(),
        'supports_visual_enhancements': supports_visual_enhancements(),
        'should_use_fallback': should_use_fallback_display(),
    }