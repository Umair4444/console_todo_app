"""
Unit tests for color support functionality.
"""
import pytest
from unittest.mock import Mock, patch
from rich.text import Text
from src.cli.cli_app import CLIApp
from src.models.todo_item import TodoItem
from src.services.visual_element_service import VisualElementService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility


class TestColorSupport:
    """
    Test class for color support functionality.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock service
        self.mock_service = Mock()
        self.app = CLIApp(service=self.mock_service)

    def test_visual_element_service_returns_correct_colors(self):
        """
        Test that VisualElementService returns correct colors for different states.
        """
        # Create a compatibility service that supports both color and emoji
        mock_compat_service = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        
        # Test completed task color
        completed_visual = visual_service.get_visual_representation('completed')
        assert 'green' in completed_visual  # Should contain green color code
        
        # Test active task color
        active_visual = visual_service.get_visual_representation('active')
        assert 'blue' in active_visual  # Should contain blue color code
        
        # Test in-progress task color
        in_progress_visual = visual_service.get_visual_representation('in_progress')
        assert 'yellow' in in_progress_visual  # Should contain yellow color code

    def test_visual_element_service_returns_correct_colors_without_color_support(self):
        """
        Test that VisualElementService returns correct representations when color is not supported.
        """
        # Create a compatibility service that supports emoji but not color
        mock_compat_service = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        
        # Test completed task - should have emoji but no color
        completed_visual = visual_service.get_visual_representation('completed')
        assert '✅' in completed_visual  # Should contain emoji
        assert '[green]' not in completed_visual  # Should not contain color code

    def test_visual_element_service_returns_fallback_without_emoji_support(self):
        """
        Test that VisualElementService returns fallback when neither emoji nor color is supported.
        """
        # Create a compatibility service that supports neither emoji nor color
        mock_compat_service = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        
        # Test completed task - should have fallback symbol
        completed_visual = visual_service.get_visual_representation('completed')
        assert '[X]' in completed_visual  # Should contain fallback symbol
        assert '✅' not in completed_visual  # Should not contain emoji

    def test_format_task_with_visuals_includes_colors_when_supported(self):
        """
        Test that format_task_with_visuals includes colors when supported.
        """
        # Create a compatibility service that supports both color and emoji
        mock_compat_service = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        
        # Format a completed task
        formatted_task = visual_service.format_task_with_visuals(1, "Test task", True)
        assert '✅' in formatted_task  # Should contain emoji
        assert '[green]' in formatted_task  # Should contain color code

    def test_format_task_with_visuals_uses_fallback_when_no_support(self):
        """
        Test that format_task_with_visuals uses fallback when no support.
        """
        # Create a compatibility service that supports neither color nor emoji
        mock_compat_service = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        
        # Format a completed task
        formatted_task = visual_service.format_task_with_visuals(1, "Test task", True)
        assert '[X]' in formatted_task  # Should contain fallback symbol
        assert '✅' not in formatted_task  # Should not contain emoji

    @patch('src.cli.cli_app.console')
    def test_cli_handles_colors_properly(self, mock_console):
        """
        Test that CLI properly handles colors in its output.
        """
        # Mock the service to return some tasks
        mock_tasks = [
            TodoItem(id=1, description="Completed task", completed=True),
            TodoItem(id=2, description="Active task", completed=False),
        ]
        self.mock_service.get_all_tasks.return_value = mock_tasks
        
        # Call the _handle_menu_list method which uses rich formatting with colors
        self.app._handle_menu_list()
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called

    def test_visual_element_service_supports_visual_enhancements_method(self):
        """
        Test the supports_visual_enhancements method of VisualElementService.
        """
        # Create a compatibility service that supports both color and emoji
        mock_compat_service = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.should_use_fallback_display.return_value = False
        
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        assert visual_service.supports_visual_enhancements() is True

        # Create a compatibility service that doesn't support both color and emoji
        mock_compat_service.should_use_fallback_display.return_value = True
        assert visual_service.supports_visual_enhancements() is False