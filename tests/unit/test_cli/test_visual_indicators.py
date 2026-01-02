"""
Unit tests for visual indicators.
"""
import pytest
from unittest.mock import Mock, patch
from rich.text import Text
from src.cli.cli_app import CLIApp
from src.models.todo_item import TodoItem
from src.services.visual_element_service import VisualElementService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility, ApplicationState


class TestVisualIndicators:
    """
    Test class for visual indicators.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock service
        self.mock_service = Mock()
        self.app = CLIApp(service=self.mock_service)

    def test_visual_element_service_gets_correct_visual_elements(self):
        """
        Test that VisualElementService returns correct visual elements.
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
        
        # Test getting a visual element
        element = visual_service.get_visual_element('completed')
        assert element.emoji == '✅'
        assert element.color == 'green'
        assert element.symbol == '[X]'
        assert element.description == 'Task completed'

    def test_visual_element_service_gets_visual_representation(self):
        """
        Test that VisualElementService returns correct visual representation.
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
        
        # Test getting visual representation
        visual = visual_service.get_visual_representation('completed')
        assert '✅' in visual  # Should contain emoji
        assert 'green' in visual  # Should contain color code

    def test_visual_element_service_gets_todo_status_visual(self):
        """
        Test that VisualElementService returns correct visual for todo status.
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
        
        # Test completed task
        visual = visual_service.get_todo_status_visual(completed=True)
        assert '✅' in visual  # Should contain completed emoji

        # Test active task
        visual = visual_service.get_todo_status_visual(completed=False, in_progress=False)
        assert '📝' in visual  # Should contain active emoji

        # Test in-progress task
        visual = visual_service.get_todo_status_visual(completed=False, in_progress=True)
        assert '🔄' in visual  # Should contain in-progress emoji

    def test_application_state_model_validates_correctly(self):
        """
        Test that ApplicationState model validates correctly.
        """
        # Test valid application state
        app_state = ApplicationState(
            current_menu='main_menu',
            waiting_for_confirmation=False,
            last_key_press='x'
        )
        assert app_state.current_menu == 'main_menu'
        assert app_state.waiting_for_confirmation is False
        assert app_state.last_key_press == 'x'

        # Test valid application state with None last_key_press
        app_state = ApplicationState(
            current_menu='main_menu',
            waiting_for_confirmation=True
        )
        assert app_state.current_menu == 'main_menu'
        assert app_state.waiting_for_confirmation is True
        assert app_state.last_key_press is None

    def test_application_state_model_validation_fails_with_empty_menu(self):
        """
        Test that ApplicationState model validation fails with empty menu.
        """
        with pytest.raises(ValueError, match="Current menu cannot be empty"):
            ApplicationState(
                current_menu='',
                waiting_for_confirmation=False
            )

    @patch('src.cli.cli_app.console')
    def test_cli_shows_visual_indicators_for_different_states(self, mock_console):
        """
        Test that CLI shows visual indicators for different application states.
        """
        # Set the app to waiting for confirmation state
        self.app.waiting_for_confirmation = True
        
        # Call process_menu_selection which should show different indicators based on state
        self.app.process_menu_selection('invalid')
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called

    @patch('src.cli.cli_app.console')
    def test_cli_shows_visual_indicators_for_error_states(self, mock_console):
        """
        Test that CLI shows visual indicators for error states.
        """
        # Mock the service to raise an exception
        self.mock_service.add_task.side_effect = Exception("Test error")
        
        # Call _handle_menu_add which should show error indicators
        with patch('builtins.input', side_effect=['Test task']):
            self.app._handle_menu_add()
        
        # Verify that console.print was called with error formatting
        print_calls = [str(call) for call, _ in mock_console.print.call_args_list]
        error_found = any("Error" in call for call in print_calls)
        assert error_found, "Error message should be displayed with formatting"

    def test_visual_element_service_gets_visual_elements_list(self):
        """
        Test that VisualElementService returns a list of visual elements.
        """
        # Create a compatibility service
        mock_compat_service = Mock()
        visual_service = VisualElementService(compatibility_service=mock_compat_service)
        
        # Get the list of visual elements
        elements_list = visual_service.get_visual_elements_list()
        
        # Verify it's a list and has elements
        assert isinstance(elements_list, list)
        assert len(elements_list) > 0
        # Verify all elements are VisualElement instances
        from src.models.visual_elements import VisualElement
        assert all(isinstance(element, VisualElement) for element in elements_list)