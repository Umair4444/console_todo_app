"""
Terminal Compatibility Service for detecting and managing terminal capabilities.
"""
from typing import Dict, Any
from src.models.visual_elements import TerminalCompatibility
from src.services.terminal_compatibility_detector import TerminalCompatibilityDetector


class TerminalCompatibilityService:
    """
    Service class that manages terminal compatibility detection and related operations.
    """

    def __init__(self):
        """
        Initialize the Terminal Compatibility Service.
        """
        self.detector = TerminalCompatibilityDetector()
        self._cached_compatibility = None

    def get_terminal_compatibility(self) -> TerminalCompatibility:
        """
        Get the terminal compatibility information.

        Returns:
            TerminalCompatibility instance with detected capabilities
        """
        # Check if we have cached compatibility info
        if self._cached_compatibility is None:
            self._cached_compatibility = self.detector.detect_compatibility()
        
        return self._cached_compatibility

    def refresh_compatibility(self) -> TerminalCompatibility:
        """
        Refresh the cached terminal compatibility information.

        Returns:
            TerminalCompatibility instance with updated capabilities
        """
        self._cached_compatibility = self.detector.detect_compatibility()
        return self._cached_compatibility

    def supports_color(self) -> bool:
        """
        Check if the terminal supports color.

        Returns:
            True if color is supported, False otherwise
        """
        compat = self.get_terminal_compatibility()
        return compat.supports_color

    def supports_emoji(self) -> bool:
        """
        Check if the terminal supports emojis.

        Returns:
            True if emoji is supported, False otherwise
        """
        compat = self.get_terminal_compatibility()
        return compat.supports_emoji

    def supports_keyboard(self) -> bool:
        """
        Check if the terminal supports keyboard input.

        Returns:
            True if keyboard input is supported, False otherwise
        """
        compat = self.get_terminal_compatibility()
        return compat.supports_keyboard

    def get_color_depth(self) -> int:
        """
        Get the color depth of the terminal.

        Returns:
            Color depth (32 for basic, 256 for 256-color, 16m for true color)
        """
        compat = self.get_terminal_compatibility()
        return compat.color_depth

    def get_encoding(self) -> str:
        """
        Get the terminal's encoding.

        Returns:
            Encoding string (e.g., 'utf-8')
        """
        compat = self.get_terminal_compatibility()
        return compat.encoding

    def get_compatibility_report(self) -> Dict[str, Any]:
        """
        Get a detailed report of terminal compatibility.

        Returns:
            Dictionary with detailed compatibility information
        """
        return self.detector.get_compatibility_report()

    def should_use_fallback_display(self) -> bool:
        """
        Determine if fallback display should be used based on terminal capabilities.

        Returns:
            True if fallback display should be used, False otherwise
        """
        compat = self.get_terminal_compatibility()
        # Use fallback if the terminal doesn't support emojis or color
        return not (compat.supports_emoji and compat.supports_color)