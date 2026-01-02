"""
Unit tests for the Visual Element Service.
"""
import pytest
from unittest.mock import Mock
from src.services.visual_element_service import VisualElementService
from src.models.visual_elements import VisualElement, TerminalCompatibility


class TestVisualElementService:
    """
    Test class for Visual Element Service.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service
        self.mock_compatibility_service = Mock()
        self.service = VisualElementService(self.mock_compatibility_service)

    def test_get_visual_element_returns_visual_element_instance(self):
        """
        Test that get_visual_element returns a VisualElement instance.
        """
        element = self.service.get_visual_element('completed')
        assert isinstance(element, VisualElement)
        assert element.emoji == '✅'
        assert element.color == 'green'
        assert element.symbol == '[X]'
        assert element.description == 'Task completed'

    def test_get_visual_element_with_unknown_type_returns_default_values(self):
        """
        Test that get_visual_element returns default values for unknown types.
        """
        element = self.service.get_visual_element('unknown_type')
        assert element.emoji == '❓'
        assert element.color == 'white'
        assert element.symbol == '[?]'
        assert element.description == 'Unknown element'

    def test_get_visual_representation_with_emoji_and_color_support(self):
        """
        Test that get_visual_representation returns emoji with color when supported.
        """
        # Mock compatibility service to indicate emoji and color support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compatibility_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.service.get_visual_representation('completed')
        assert '✅' in result  # Should contain the emoji
        assert '[green]' in result  # Should contain the color code

    def test_get_visual_representation_with_emoji_only_support(self):
        """
        Test that get_visual_representation returns emoji without color when only emoji is supported.
        """
        # Mock compatibility service to indicate emoji support but no color support
        mock_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        self.mock_compatibility_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.service.get_visual_representation('completed')
        assert '✅' in result  # Should contain the emoji
        assert '[green]' not in result  # Should not contain color code

    def test_get_visual_representation_with_no_emoji_support(self):
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
        self.mock_compatibility_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.service.get_visual_representation('completed')
        assert '[X]' in result  # Should contain the fallback symbol
        assert '✅' not in result  # Should not contain the emoji

    def test_get_todo_status_visual_returns_correct_visual(self):
        """
        Test that get_todo_status_visual returns the correct visual based on status.
        """
        # Mock compatibility service to indicate full support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compatibility_service.get_terminal_compatibility.return_value = mock_compat
        
        # Test completed task
        result = self.service.get_todo_status_visual(completed=True)
        assert '✅' in result  # Should contain completed emoji

        # Test active task
        result = self.service.get_todo_status_visual(completed=False, in_progress=False)
        assert '📝' in result  # Should contain active emoji

        # Test in-progress task
        result = self.service.get_todo_status_visual(completed=False, in_progress=True)
        assert '🔄' in result  # Should contain in-progress emoji

    def test_get_todo_status_fallback_returns_correct_fallback(self):
        """
        Test that get_todo_status_fallback returns the correct fallback symbol.
        """
        # Test completed task
        result = self.service.get_todo_status_fallback(completed=True)
        assert result == '[X]'

        # Test active task
        result = self.service.get_todo_status_fallback(completed=False, in_progress=False)
        assert result == '[O]'

        # Test in-progress task
        result = self.service.get_todo_status_fallback(completed=False, in_progress=True)
        assert result == '[~]'

    def test_format_task_with_visuals_formats_correctly(self):
        """
        Test that format_task_with_visuals formats correctly based on terminal capabilities.
        """
        # Mock compatibility service to indicate full support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compatibility_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.service.format_task_with_visuals(1, "Test task", False)
        assert '📝' in result  # Should contain the active task emoji
        assert "1. Test task" in result

        result = self.service.format_task_with_visuals(2, "Completed task", True)
        assert '✅' in result  # Should contain the completed task emoji
        assert "2. Completed task" in result

    def test_get_menu_option_visual_formats_correctly(self):
        """
        Test that get_menu_option_visual formats menu options correctly.
        """
        # Mock compatibility service to indicate full support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compatibility_service.get_terminal_compatibility.return_value = mock_compat
        
        result = self.service.get_menu_option_visual('add_task', 'Add New Task')
        assert '➕' in result  # Should contain the add emoji
        assert "Add New Task" in result

        result = self.service.get_menu_option_visual('list_tasks', 'List All Tasks')
        assert '📋' in result  # Should contain the list emoji
        assert "List All Tasks" in result

    def test_get_visual_elements_list_returns_list_of_visual_elements(self):
        """
        Test that get_visual_elements_list returns a list of VisualElement instances.
        """
        elements = self.service.get_visual_elements_list()
        
        assert isinstance(elements, list)
        assert len(elements) > 0  # Should have at least one element
        assert all(isinstance(element, VisualElement) for element in elements)

    def test_supports_visual_enhancements_returns_correct_value(self):
        """
        Test that supports_visual_enhancements returns the correct value.
        """
        # Mock compatibility service to indicate no fallback needed (visuals supported)
        self.mock_compatibility_service.should_use_fallback_display.return_value = False
        result = self.service.supports_visual_enhancements()
        assert result is True

        # Mock compatibility service to indicate fallback needed (visuals not supported)
        self.mock_compatibility_service.should_use_fallback_display.return_value = True
        result = self.service.supports_visual_enhancements()
        assert result is False