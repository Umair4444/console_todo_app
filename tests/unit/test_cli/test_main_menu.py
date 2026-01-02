"""
Unit tests for main menu visual enhancements.
"""
import pytest
from unittest.mock import Mock, patch
from rich.table import Table
from src.cli.cli_app import CLIApp


class TestMainMenuVisualEnhancements:
    """
    Test class for main menu visual enhancements.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock service
        self.mock_service = Mock()
        self.app = CLIApp(service=self.mock_service)

    @patch('src.cli.cli_app.console')
    def test_display_menu_shows_rich_formatted_table(self, mock_console):
        """
        Test that display_menu shows a rich formatted table with emojis.
        """
        # Call the display_menu method
        self.app.display_menu()
        
        # Verify that console methods were called appropriately
        assert mock_console.clear.called
        assert mock_console.rule.called
        # Check that print was called with a Table object (indicating rich formatting)
        assert any(isinstance(call_arg, Table) for call_arg, _ in mock_console.print.call_args_list)

    @patch('src.cli.cli_app.console')
    def test_display_menu_includes_emojis_in_options(self, mock_console):
        """
        Test that display_menu includes emojis in menu options.
        """
        # Call the display_menu method
        self.app.display_menu()
        
        # Capture the calls to console.print to check for emojis
        print_calls = [str(call) for call, _ in mock_console.print.call_args_list]
        # Check that some calls contain emojis
        has_emojis = any(emoji in str(call) for call in print_calls for emoji in ['➕', '📋', '✏️', '🗑️', '✅', '↩️', '📤', '📥', '🚪'])
        assert has_emojis, "Menu should contain emojis"

    @patch('src.cli.cli_app.console')
    def test_display_menu_includes_formatted_status(self, mock_console):
        """
        Test that display_menu includes formatted status information.
        """
        # Set some status for the app
        self.app.waiting_for_confirmation = True
        
        # Call the display_menu method
        self.app.display_menu()
        
        # Check that the status information was printed
        print_calls = [str(call) for call, _ in mock_console.print.call_args_list]
        status_found = any("Current status:" in call for call in print_calls)
        assert status_found, "Status information should be displayed"

    @patch('src.cli.cli_app.console')
    def test_run_menu_loop_shows_formatted_welcome_message(self, mock_console):
        """
        Test that run_menu_loop shows formatted welcome message.
        """
        # Set the app to run only once then stop
        original_running = self.app.running
        self.app.running = True
        
        # Mock the input to exit immediately
        with patch('builtins.input', side_effect=['9']):
            self.app.run_menu_loop()
        
        # Reset running state
        self.app.running = original_running
        
        # Verify that formatted welcome message was printed
        print_calls = [str(call) for call, _ in mock_console.print.call_args_list]
        welcome_found = any("Welcome to the To-Do List Application!" in call for call in print_calls)
        assert welcome_found, "Welcome message should be displayed with formatting"

    @patch('src.cli.cli_app.console')
    def test_process_menu_selection_shows_formatted_error_messages(self, mock_console):
        """
        Test that process_menu_selection shows formatted error messages.
        """
        # Call process_menu_selection with invalid input
        self.app.process_menu_selection("invalid")
        
        # Verify that error message was printed with formatting
        print_calls = [str(call) for call, _ in mock_console.print.call_args_list]
        error_found = any("Invalid option" in call for call in print_calls)
        assert error_found, "Error message should be displayed with formatting"

    def test_menu_visuals_match_expected_values(self):
        """
        Test that menu visuals match expected values.
        """
        # This test verifies that the menu options have the expected emojis
        # by checking the source code implementation indirectly
        import inspect
        source = inspect.getsource(self.app.display_menu)
        
        # Check that the source contains expected emojis
        expected_emojis = ['➕', '📋', '✏️', '🗑️', '✅', '↩️', '📤', '📥', '🚪']
        for emoji in expected_emojis:
            assert emoji in source, f"Menu should contain {emoji} emoji"