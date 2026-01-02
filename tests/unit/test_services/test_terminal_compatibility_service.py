"""
Unit tests for the Terminal Compatibility Service.
"""
import pytest
from unittest.mock import Mock
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility


class TestTerminalCompatibilityService:
    """
    Test class for Terminal Compatibility Service.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock detector to control the behavior
        self.mock_detector = Mock()
        self.service = TerminalCompatibilityService()
        # Replace the detector with our mock
        self.service.detector = self.mock_detector

    def test_get_terminal_compatibility_returns_terminal_compatibility_instance(self):
        """
        Test that get_terminal_compatibility returns a TerminalCompatibility instance.
        """
        # Set up the mock to return a specific compatibility
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        compat = self.service.get_terminal_compatibility()
        
        assert isinstance(compat, TerminalCompatibility)
        assert compat.supports_color == expected_compat.supports_color
        assert compat.supports_emoji == expected_compat.supports_emoji
        assert compat.supports_keyboard == expected_compat.supports_keyboard
        assert compat.color_depth == expected_compat.color_depth
        assert compat.encoding == expected_compat.encoding

    def test_refresh_compatibility_updates_cached_compatibility(self):
        """
        Test that refresh_compatibility updates the cached compatibility.
        """
        # Set up the mock to return different compatibilities
        first_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        second_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=False,
            color_depth=32,
            encoding='ascii'
        )
        
        self.mock_detector.detect_compatibility.side_effect = [first_compat, second_compat]
        
        # Get the first compatibility
        first_result = self.service.get_terminal_compatibility()
        assert first_result.supports_color == True
        
        # Refresh and get the second compatibility
        second_result = self.service.refresh_compatibility()
        assert second_result.supports_color == False

    def test_supports_color_returns_correct_value(self):
        """
        Test that supports_color returns the correct value.
        """
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.supports_color()
        assert result == True

    def test_supports_emoji_returns_correct_value(self):
        """
        Test that supports_emoji returns the correct value.
        """
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.supports_emoji()
        assert result == False

    def test_supports_keyboard_returns_correct_value(self):
        """
        Test that supports_keyboard returns the correct value.
        """
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=False,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.supports_keyboard()
        assert result == False

    def test_get_color_depth_returns_correct_value(self):
        """
        Test that get_color_depth returns the correct value.
        """
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=16777216,  # 16m color
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.get_color_depth()
        assert result == 16777216

    def test_get_encoding_returns_correct_value(self):
        """
        Test that get_encoding returns the correct value.
        """
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='ascii'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.get_encoding()
        assert result == 'ascii'

    def test_should_use_fallback_display_returns_true_when_no_emoji_or_color(self):
        """
        Test that should_use_fallback_display returns True when no emoji or color support.
        """
        # No emoji support
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.should_use_fallback_display()
        assert result == True

        # No color support
        expected_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.should_use_fallback_display()
        assert result == True

        # Both emoji and color support
        expected_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_detector.detect_compatibility.return_value = expected_compat
        
        result = self.service.should_use_fallback_display()
        assert result == False