"""
Unit tests for the Emoji Mapping Service.
"""
import pytest
from unittest.mock import Mock
from src.services.emoji_mapping_service import EmojiMappingService
from src.models.visual_elements import TerminalCompatibility


class TestEmojiMappingService:
    """
    Test class for Emoji Mapping Service.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create mock services
        self.mock_compatibility_service = Mock()
        self.mock_visual_element_service = Mock()
        self.service = EmojiMappingService(
            compatibility_service=self.mock_compatibility_service,
            visual_element_service=self.mock_visual_element_service
        )

    def test_get_emoji_for_state_returns_correct_emoji_with_emoji_support(self):
        """
        Test that get_emoji_for_state returns correct emoji when emoji is supported.
        """
        # Mock compatibility service to indicate emoji support
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compatibility_service.supports_emoji.return_value = True
        
        result = self.service.get_emoji_for_state('completed')
        assert result == '✅'

        result = self.service.get_emoji_for_state('active')
        assert result == '📝'

        result = self.service.get_emoji_for_state('in_progress')
        assert result == '🔄'

    def test_get_emoji_for_state_returns_correct_fallback_without_emoji_support(self):
        """
        Test that get_emoji_for_state returns correct fallback when emoji is not supported.
        """
        # Mock compatibility service to indicate no emoji support
        self.mock_compatibility_service.supports_emoji.return_value = False
        
        result = self.service.get_emoji_for_state('completed')
        assert result == '[X]'

        result = self.service.get_emoji_for_state('active')
        assert result == '[O]'

        result = self.service.get_emoji_for_state('in_progress')
        assert result == '[~]'

    def test_get_emoji_for_state_returns_default_for_unknown_state_with_emoji_support(self):
        """
        Test that get_emoji_for_state returns default for unknown state with emoji support.
        """
        # Mock compatibility service to indicate emoji support
        self.mock_compatibility_service.supports_emoji.return_value = True
        
        result = self.service.get_emoji_for_state('unknown_state')
        assert result == '📝'  # Should return 'active' as default

    def test_get_emoji_for_state_returns_default_for_unknown_state_without_emoji_support(self):
        """
        Test that get_emoji_for_state returns default for unknown state without emoji support.
        """
        # Mock compatibility service to indicate no emoji support
        self.mock_compatibility_service.supports_emoji.return_value = False
        
        result = self.service.get_emoji_for_state('unknown_state')
        assert result == '[O]'  # Should return 'active' fallback as default

    def test_get_visual_for_todo_status_returns_correct_visual(self):
        """
        Test that get_visual_for_todo_status returns correct visual based on status.
        """
        # Mock compatibility service to indicate emoji support
        self.mock_compatibility_service.supports_emoji.return_value = True
        
        # Test completed task
        result = self.service.get_visual_for_todo_status(completed=True)
        assert result == '✅'

        # Test active task
        result = self.service.get_visual_for_todo_status(completed=False, in_progress=False)
        assert result == '📝'

        # Test in-progress task
        result = self.service.get_visual_for_todo_status(completed=False, in_progress=True)
        assert result == '🔄'

        # Test high priority task
        result = self.service.get_visual_for_todo_status(completed=False, priority='high')
        assert result == '❗'

        # Test low priority task
        result = self.service.get_visual_for_todo_status(completed=False, priority='low')
        assert result == '🔽'

    def test_get_emoji_for_task_operation_returns_correct_emoji_with_emoji_support(self):
        """
        Test that get_emoji_for_task_operation returns correct emoji when supported.
        """
        # Mock compatibility service to indicate emoji support
        self.mock_compatibility_service.supports_emoji.return_value = True
        
        result = self.service.get_emoji_for_task_operation('add')
        assert result == '➕'

        result = self.service.get_emoji_for_task_operation('list')
        assert result == '📋'

        result = self.service.get_emoji_for_task_operation('delete')
        assert result == '🗑️'

    def test_get_emoji_for_task_operation_returns_correct_fallback_without_emoji_support(self):
        """
        Test that get_emoji_for_task_operation returns correct fallback when not supported.
        """
        # Mock compatibility service to indicate no emoji support
        self.mock_compatibility_service.supports_emoji.return_value = False
        
        result = self.service.get_emoji_for_task_operation('add')
        assert result == '[+]'

        result = self.service.get_emoji_for_task_operation('list')
        assert result == '[L]'

        result = self.service.get_emoji_for_task_operation('delete')
        assert result == '[DEL]'

    def test_get_available_states_returns_correct_dict_with_emoji_support(self):
        """
        Test that get_available_states returns correct dict when emoji is supported.
        """
        # Mock compatibility service to indicate emoji support
        self.mock_compatibility_service.supports_emoji.return_value = True
        
        result = self.service.get_available_states()
        assert 'completed' in result
        assert result['completed'] == '✅'

    def test_get_available_states_returns_correct_dict_without_emoji_support(self):
        """
        Test that get_available_states returns correct dict when emoji is not supported.
        """
        # Mock compatibility service to indicate no emoji support
        self.mock_compatibility_service.supports_emoji.return_value = False
        
        result = self.service.get_available_states()
        assert 'completed' in result
        assert result['completed'] == '[X]'

    def test_get_available_operations_returns_correct_dict_with_emoji_support(self):
        """
        Test that get_available_operations returns correct dict when emoji is supported.
        """
        # Mock compatibility service to indicate emoji support
        self.mock_compatibility_service.supports_emoji.return_value = True
        
        result = self.service.get_available_operations()
        assert 'add' in result
        assert result['add'] == '➕'

    def test_get_available_operations_returns_correct_dict_without_emoji_support(self):
        """
        Test that get_available_operations returns correct dict when emoji is not supported.
        """
        # Mock compatibility service to indicate no emoji support
        self.mock_compatibility_service.supports_emoji.return_value = False
        
        result = self.service.get_available_operations()
        assert 'add' in result
        assert result['add'] == '[+]'

    def test_is_state_valid_returns_correct_value(self):
        """
        Test that is_state_valid returns correct value for valid and invalid states.
        """
        # Test valid state
        result = self.service.is_state_valid('completed')
        assert result is True

        # Test invalid state
        result = self.service.is_state_valid('invalid_state')
        assert result is False