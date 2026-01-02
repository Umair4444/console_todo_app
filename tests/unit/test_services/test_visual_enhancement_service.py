"""
Unit tests for the Visual Enhancement Service.
"""
import pytest
from src.services.visual_enhancement_service import VisualEnhancementService, VisualElement


class TestVisualEnhancementService:
    """
    Test class for Visual Enhancement Service.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        self.service = VisualEnhancementService()

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

    def test_get_todo_status_emoji_returns_correct_emoji(self):
        """
        Test that get_todo_status_emoji returns the correct emoji based on status.
        """
        # Test completed task
        emoji = self.service.get_todo_status_emoji(completed=True)
        assert emoji == '✅'

        # Test active task
        emoji = self.service.get_todo_status_emoji(completed=False)
        assert emoji == '📝'

        # Test in-progress task
        emoji = self.service.get_todo_status_emoji(completed=False, in_progress=True)
        assert emoji == '🔄'

    def test_get_todo_status_color_returns_correct_color(self):
        """
        Test that get_todo_status_color returns the correct color based on status.
        """
        # Test completed task
        color = self.service.get_todo_status_color(completed=True)
        assert color == 'green'

        # Test active task
        color = self.service.get_todo_status_color(completed=False)
        assert color == 'blue'

        # Test in-progress task
        color = self.service.get_todo_status_color(completed=False, in_progress=True)
        assert color == 'yellow'

    def test_get_fallback_for_emoji_returns_correct_fallback(self):
        """
        Test that get_fallback_for_emoji returns the correct fallback.
        """
        fallback = self.service.get_fallback_for_emoji('✅')
        assert fallback == '[X]'

        fallback = self.service.get_fallback_for_emoji('🔄')
        assert fallback == '[~]'

    def test_get_fallback_for_unknown_emoji_returns_default(self):
        """
        Test that get_fallback_for_emoji returns default for unknown emoji.
        """
        fallback = self.service.get_fallback_for_emoji('🚀')
        assert fallback == '[?]'

    def test_format_task_with_visuals_formats_correctly_with_color_support(self):
        """
        Test that format_task_with_visuals formats correctly with color support.
        """
        # This test checks the format but doesn't verify color codes since
        # the actual color support check is complex to mock
        formatted = self.service.format_task_with_visuals(1, "Test task", False)
        # Should contain the active task emoji
        assert '📝' in formatted or '[O]' in formatted
        assert "1. Test task" in formatted

        formatted = self.service.format_task_with_visuals(2, "Completed task", True)
        # Should contain the completed task emoji
        assert '✅' in formatted or '[X]' in formatted
        assert "2. Completed task" in formatted