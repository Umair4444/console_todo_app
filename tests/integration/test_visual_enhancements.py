"""
Integration tests for visual enhancements.
"""
import pytest
from unittest.mock import Mock, patch
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.models.todo_item import TodoItem
from src.services.visual_element_service import VisualElementService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility


class TestVisualEnhancementsIntegration:
    """
    Integration test class for visual enhancements.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock todo service
        self.mock_todo_service = Mock(spec=TodoService)
        self.app = CLIApp(service=self.mock_todo_service)

    @patch('src.cli.cli_app.console')
    def test_full_menu_flow_with_visual_enhancements(self, mock_console):
        """
        Test a full menu flow with visual enhancements.
        """
        # Mock the service to return some tasks
        mock_tasks = [
            TodoItem(id=1, description="Completed task", completed=True),
            TodoItem(id=2, description="Active task", completed=False),
        ]
        self.mock_todo_service.get_all_tasks.return_value = mock_tasks
        
        # Simulate the menu display
        self.app.display_menu()
        
        # Verify rich formatting was used
        assert mock_console.clear.called or mock_console.rule.called
        
        # Simulate listing tasks
        self.app._handle_menu_list()
        
        # Verify that the list was displayed with rich formatting
        assert mock_console.print.called

    @patch('src.cli.cli_app.console')
    def test_add_task_flow_with_visual_enhancements(self, mock_console):
        """
        Test the add task flow with visual enhancements.
        """
        # Mock the service to return a task
        mock_task = TodoItem(id=1, description="New task", completed=False)
        self.mock_todo_service.add_task.return_value = mock_task
        
        # Simulate adding a task
        with patch('builtins.input', side_effect=['New task description']):
            self.app._handle_menu_add()
        
        # Verify that success message was displayed with rich formatting
        assert any("Added task" in str(call) for call, _ in mock_console.print.call_args_list)

    @patch('src.cli.cli_app.console')
    def test_complete_task_flow_with_visual_enhancements(self, mock_console):
        """
        Test the complete task flow with visual enhancements.
        """
        # Mock the service to return a task
        mock_task = TodoItem(id=1, description="Task to complete", completed=True)
        self.mock_todo_service.mark_task_complete.return_value = mock_task
        
        # Simulate completing a task
        with patch('builtins.input', side_effect=['1']):
            self.app._handle_menu_complete()
        
        # Verify that success message was displayed with rich formatting
        assert any("Marked task" in str(call) for call, _ in mock_console.print.call_args_list)

    @patch('src.cli.cli_app.console')
    def test_visual_enhancement_services_work_together(self, mock_console):
        """
        Test that visual enhancement services work together correctly.
        """
        # Create real compatibility service with mock detector
        from unittest.mock import Mock
        mock_detector = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_detector.detect_compatibility.return_value = mock_compat
        
        from src.services.terminal_compatibility_detector import TerminalCompatibilityDetector
        # We'll create a mock that behaves like the real detector
        compat_service = TerminalCompatibilityService()
        compat_service.detector = mock_detector
        
        # Create visual element service with the compatibility service
        visual_service = VisualElementService(compatibility_service=compat_service)
        
        # Test that they work together
        visual_repr = visual_service.get_visual_representation('completed')
        assert '✅' in visual_repr  # Should contain emoji
        assert 'green' in visual_repr  # Should contain color code

    @patch('src.cli.cli_app.console')
    def test_cli_handles_different_terminal_compatibility_scenarios(self, mock_console):
        """
        Test that CLI handles different terminal compatibility scenarios.
        """
        # Test with full support
        from unittest.mock import Mock
        mock_compat_service = Mock()
        full_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = full_compat
        
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        
        # Test visual representation with full support
        full_visual = visual_service.get_visual_representation('active')
        assert '📝' in full_visual  # Should contain emoji
        
        # Test with no support
        no_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = no_compat
        
        # Test visual representation with no support
        no_visual = visual_service.get_visual_representation('active')
        assert '[O]' in no_visual  # Should contain fallback
        assert '📝' not in no_visual  # Should not contain emoji

    @patch('src.cli.cli_app.console')
    def test_menu_selection_with_visual_feedback(self, mock_console):
        """
        Test menu selection with visual feedback.
        """
        # Test valid selection
        self.app.process_menu_selection('1')  # Add task option
        
        # Verify that the appropriate handler was called (indirectly through rich output)
        # The handler would call console.print for errors or success
        
        # Test invalid selection
        self.app.process_menu_selection('99')
        
        # Verify error message was displayed with rich formatting
        assert any("Invalid option" in str(call) for call, _ in mock_console.print.call_args_list)

    def test_visual_enhancement_services_integration_with_models(self):
        """
        Test that visual enhancement services integrate properly with models.
        """
        # Create real services and models to test integration
        from unittest.mock import Mock
        mock_detector = Mock()
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_detector.detect_compatibility.return_value = mock_compat
        
        compat_service = TerminalCompatibilityService()
        compat_service.detector = mock_detector
        
        visual_service = VisualElementService(compatibility_service=compat_service)
        
        # Test integration by getting a visual element
        element = visual_service.get_visual_element('completed')
        
        # Verify it's a VisualElement model instance
        from src.models.visual_elements import VisualElement
        assert isinstance(element, VisualElement)
        assert element.emoji == '✅'
        assert element.color == 'green'
        assert element.symbol == '[X]'
        assert element.description == 'Task completed'