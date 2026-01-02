"""
Unit tests for emoji mapping functionality.
"""
import pytest
from src.services.emoji_mapping_service import EmojiMappingService
from src.models.visual_elements import TerminalCompatibility


class TestEmojiMapping:
    """
    Test class for emoji mapping functionality.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service that supports emojis
        from unittest.mock import Mock
        self.mock_compatibility_service = Mock()
        self.mock_compatibility_service.supports_emoji.return_value = True
        self.service = EmojiMappingService(compatibility_service=self.mock_compatibility_service)

    def test_get_emoji_for_completed_state(self):
        """
        Test that the correct emoji is returned for completed state.
        """
        emoji = self.service.get_emoji_for_state('completed')
        assert emoji == '✅'

    def test_get_emoji_for_active_state(self):
        """
        Test that the correct emoji is returned for active state.
        """
        emoji = self.service.get_emoji_for_state('active')
        assert emoji == '📝'

    def test_get_emoji_for_in_progress_state(self):
        """
        Test that the correct emoji is returned for in-progress state.
        """
        emoji = self.service.get_emoji_for_state('in_progress')
        assert emoji == '🔄'

    def test_get_emoji_for_deleted_state(self):
        """
        Test that the correct emoji is returned for deleted state.
        """
        emoji = self.service.get_emoji_for_state('deleted')
        assert emoji == '❌'

    def test_get_emoji_for_pending_state(self):
        """
        Test that the correct emoji is returned for pending state.
        """
        emoji = self.service.get_emoji_for_state('pending')
        assert emoji == '⏳'

    def test_get_emoji_for_high_priority_state(self):
        """
        Test that the correct emoji is returned for high priority state.
        """
        emoji = self.service.get_emoji_for_state('high_priority')
        assert emoji == '❗'

    def test_get_emoji_for_low_priority_state(self):
        """
        Test that the correct emoji is returned for low priority state.
        """
        emoji = self.service.get_emoji_for_state('low_priority')
        assert emoji == '🔽'

    def test_get_emoji_for_unknown_state_returns_default(self):
        """
        Test that a default emoji is returned for unknown state.
        """
        emoji = self.service.get_emoji_for_state('unknown_state')
        assert emoji == '📝'  # Should return 'active' as default

    def test_get_visual_for_todo_status_completed(self):
        """
        Test that the correct visual is returned for completed todo status.
        """
        visual = self.service.get_visual_for_todo_status(completed=True)
        assert visual == '✅'

    def test_get_visual_for_todo_status_active(self):
        """
        Test that the correct visual is returned for active todo status.
        """
        visual = self.service.get_visual_for_todo_status(completed=False, in_progress=False)
        assert visual == '📝'

    def test_get_visual_for_todo_status_in_progress(self):
        """
        Test that the correct visual is returned for in-progress todo status.
        """
        visual = self.service.get_visual_for_todo_status(completed=False, in_progress=True)
        assert visual == '🔄'

    def test_get_visual_for_todo_status_high_priority(self):
        """
        Test that the correct visual is returned for high priority todo status.
        """
        visual = self.service.get_visual_for_todo_status(completed=False, priority='high')
        assert visual == '❗'

    def test_get_visual_for_todo_status_low_priority(self):
        """
        Test that the correct visual is returned for low priority todo status.
        """
        visual = self.service.get_visual_for_todo_status(completed=False, priority='low')
        assert visual == '🔽'

    def test_get_emoji_for_task_operation_add(self):
        """
        Test that the correct emoji is returned for add operation.
        """
        emoji = self.service.get_emoji_for_task_operation('add')
        assert emoji == '➕'

    def test_get_emoji_for_task_operation_list(self):
        """
        Test that the correct emoji is returned for list operation.
        """
        emoji = self.service.get_emoji_for_task_operation('list')
        assert emoji == '📋'

    def test_get_emoji_for_task_operation_update(self):
        """
        Test that the correct emoji is returned for update operation.
        """
        emoji = self.service.get_emoji_for_task_operation('update')
        assert emoji == '✏️'

    def test_get_emoji_for_task_operation_delete(self):
        """
        Test that the correct emoji is returned for delete operation.
        """
        emoji = self.service.get_emoji_for_task_operation('delete')
        assert emoji == '🗑️'

    def test_get_emoji_for_task_operation_complete(self):
        """
        Test that the correct emoji is returned for complete operation.
        """
        emoji = self.service.get_emoji_for_task_operation('complete')
        assert emoji == '✅'

    def test_get_emoji_for_task_operation_incomplete(self):
        """
        Test that the correct emoji is returned for incomplete operation.
        """
        emoji = self.service.get_emoji_for_task_operation('incomplete')
        assert emoji == '↩️'

    def test_get_emoji_for_task_operation_export(self):
        """
        Test that the correct emoji is returned for export operation.
        """
        emoji = self.service.get_emoji_for_task_operation('export')
        assert emoji == '📤'

    def test_get_emoji_for_task_operation_import(self):
        """
        Test that the correct emoji is returned for import operation.
        """
        emoji = self.service.get_emoji_for_task_operation('import')
        assert emoji == '📥'

    def test_get_emoji_for_task_operation_help(self):
        """
        Test that the correct emoji is returned for help operation.
        """
        emoji = self.service.get_emoji_for_task_operation('help')
        assert emoji == '❓'

    def test_get_emoji_for_task_operation_exit(self):
        """
        Test that the correct emoji is returned for exit operation.
        """
        emoji = self.service.get_emoji_for_task_operation('exit')
        assert emoji == '🚪'

    def test_get_emoji_for_task_operation_unknown_returns_default(self):
        """
        Test that a default emoji is returned for unknown operation.
        """
        emoji = self.service.get_emoji_for_task_operation('unknown_operation')
        assert emoji == '❓'

    def test_is_state_valid_returns_true_for_valid_state(self):
        """
        Test that is_state_valid returns True for valid states.
        """
        assert self.service.is_state_valid('completed') is True
        assert self.service.is_state_valid('active') is True
        assert self.service.is_state_valid('in_progress') is True

    def test_is_state_valid_returns_false_for_invalid_state(self):
        """
        Test that is_state_valid returns False for invalid states.
        """
        assert self.service.is_state_valid('invalid_state') is False