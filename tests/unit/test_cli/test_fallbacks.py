"""
Unit tests for emoji fallback functionality.
"""
import pytest
from unittest.mock import Mock
from src.services.visual_element_service import VisualElementService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility


class TestEmojiFallbacks:
    """
    Test class for emoji fallback functionality.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service
        self.mock_compat_service = Mock()
        self.visual_service = VisualElementService(compatibility_service=self.mock_compat_service)

    def test_get_visual_representation_returns_fallback_when_no_emoji_support(self):
        """
        Test that get_visual_representation returns fallback when no emoji support.
        """
        # Mock compatibility service to indicate no emoji support
        mock_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        self.mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        # Test completed task fallback
        result = self.visual_service.get_visual_representation('completed')
        assert '[X]' in result  # Should contain fallback symbol
        assert '✅' not in result  # Should not contain emoji

        # Test active task fallback
        result = self.visual_service.get_visual_representation('active')
        assert '[O]' in result  # Should contain fallback symbol
        assert '📝' not in result  # Should not contain emoji

        # Test in-progress task fallback
        result = self.visual_service.get_visual_representation('in_progress')
        assert '[~]' in result  # Should contain fallback symbol
        assert '🔄' not in result  # Should not contain emoji

    def test_get_visual_representation_returns_emoji_with_emoji_support(self):
        """
        Test that get_visual_representation returns emoji when emoji support is available.
        """
        # Mock compatibility service to indicate emoji support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        # Test completed task emoji
        result = self.visual_service.get_visual_representation('completed')
        assert '✅' in result  # Should contain emoji
        assert '[X]' not in result  # Should not contain fallback symbol

        # Test active task emoji
        result = self.visual_service.get_visual_representation('active')
        assert '📝' in result  # Should contain emoji
        assert '[O]' not in result  # Should not contain fallback symbol

    def test_get_todo_status_fallback_returns_correct_symbols(self):
        """
        Test that get_todo_status_fallback returns correct fallback symbols.
        """
        # This method should always return fallback symbols regardless of compatibility
        result = self.visual_service.get_todo_status_fallback(completed=True)
        assert result == '[X]'

        result = self.visual_service.get_todo_status_fallback(completed=False, in_progress=False)
        assert result == '[O]'

        result = self.visual_service.get_todo_status_fallback(completed=False, in_progress=True)
        assert result == '[~]'

    def test_format_task_with_visuals_uses_fallback_when_no_emoji_support(self):
        """
        Test that format_task_with_visuals uses fallback when no emoji support.
        """
        # Mock compatibility service to indicate no emoji support
        mock_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        self.mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.visual_service.format_task_with_visuals(1, "Test task", True)
        assert '[X]' in result  # Should contain fallback symbol
        assert '✅' not in result  # Should not contain emoji

        result = self.visual_service.format_task_with_visuals(2, "Test task", False)
        assert '[O]' in result  # Should contain fallback symbol
        assert '📝' not in result  # Should not contain emoji

    def test_format_task_with_visuals_uses_emoji_with_emoji_support(self):
        """
        Test that format_task_with_visuals uses emoji when emoji support is available.
        """
        # Mock compatibility service to indicate emoji support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.visual_service.format_task_with_visuals(1, "Test task", True)
        assert '✅' in result  # Should contain emoji
        assert '[X]' not in result  # Should not contain fallback symbol

        result = self.visual_service.format_task_with_visuals(2, "Test task", False)
        assert '📝' in result  # Should contain emoji
        assert '[O]' not in result  # Should not contain fallback symbol

    def test_get_menu_option_visual_uses_fallback_when_no_emoji_support(self):
        """
        Test that get_menu_option_visual uses fallback when no emoji support.
        """
        # Mock compatibility service to indicate no emoji support
        mock_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        self.mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.visual_service.get_menu_option_visual('add_task', 'Add New Task')
        assert '[+]' in result  # Should contain fallback symbol
        assert '➕' not in result  # Should not contain emoji

        result = self.visual_service.get_menu_option_visual('list_tasks', 'List Tasks')
        assert '[L]' in result  # Should contain fallback symbol
        assert '📋' not in result  # Should not contain emoji

    def test_get_menu_option_visual_uses_emoji_with_emoji_support(self):
        """
        Test that get_menu_option_visual uses emoji when emoji support is available.
        """
        # Mock compatibility service to indicate emoji support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.visual_service.get_menu_option_visual('add_task', 'Add New Task')
        assert '➕' in result  # Should contain emoji
        assert '[+]' not in result  # Should not contain fallback symbol

        result = self.visual_service.get_menu_option_visual('list_tasks', 'List Tasks')
        assert '📋' in result  # Should contain emoji
        assert '[L]' not in result  # Should not contain fallback symbol

    def test_supports_visual_enhancements_returns_false_when_no_emoji_or_color(self):
        """
        Test that supports_visual_enhancements returns False when no emoji or color support.
        """
        # Mock compatibility service to indicate no emoji or color support
        self.mock_compat_service.should_use_fallback_display.return_value = True
        
        result = self.visual_service.supports_visual_enhancements()
        assert result is False

    def test_supports_visual_enhancements_returns_true_when_emoji_and_color_supported(self):
        """
        Test that supports_visual_enhancements returns True when emoji and color supported.
        """
        # Mock compatibility service to indicate emoji and color support
        self.mock_compat_service.should_use_fallback_display.return_value = False
        
        result = self.visual_service.supports_visual_enhancements()
        assert result is True