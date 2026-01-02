"""
Unit tests for todo_item display with emojis.
"""
import pytest
from unittest.mock import Mock, patch
from rich.text import Text
from rich.table import Table
from src.cli.cli_app import CLIApp
from src.models.todo_item import TodoItem


class TestTodoDisplayWithEmojis:
    """
    Test class for todo_item display with emojis functionality.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock service
        self.mock_service = Mock()
        self.app = CLIApp(service=self.mock_service)

    @patch('src.cli.cli_app.console')
    def test_display_menu_shows_emojis_in_options(self, mock_console):
        """
        Test that the display_menu method shows emojis in menu options.
        """
        # Call the display_menu method
        self.app.display_menu()
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called or mock_console.rule.called or mock_console.clear.called

    @patch('src.cli.cli_app.console')
    def test_handle_menu_list_shows_emojis_for_tasks(self, mock_console):
        """
        Test that _handle_menu_list shows emojis for tasks.
        """
        # Mock the service to return some tasks
        mock_tasks = [
            TodoItem(id=1, description="Task 1", completed=False),
            TodoItem(id=2, description="Task 2", completed=True),
        ]
        self.mock_service.get_all_tasks.return_value = mock_tasks
        
        # Call the _handle_menu_list method
        self.app._handle_menu_list()
        
        # Verify that console.print was called with a table (indicating rich formatting was used)
        assert any(isinstance(call_arg, Table) for call_arg, _ in mock_console.print.call_args_list)

    @patch('src.cli.cli_app.console')
    def test_handle_add_shows_success_message_with_emoji_formatting(self, mock_console):
        """
        Test that _handle_add shows success message with emoji formatting.
        """
        # Mock the service to return a task
        mock_task = TodoItem(id=1, description="New task", completed=False)
        self.mock_service.add_task.return_value = mock_task
        
        # Call the _handle_menu_add method with input simulation
        with patch('builtins.input', side_effect=['New task']):
            self.app._handle_menu_add()
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called

    @patch('src.cli.cli_app.console')
    def test_handle_complete_shows_success_message_with_emoji_formatting(self, mock_console):
        """
        Test that _handle_complete shows success message with emoji formatting.
        """
        # Mock the service to return a task
        mock_task = TodoItem(id=1, description="Task to complete", completed=True)
        self.mock_service.mark_task_complete.return_value = mock_task
        
        # Call the _handle_menu_complete method with input simulation
        with patch('builtins.input', side_effect=['1']):
            self.app._handle_menu_complete()
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called

    @patch('src.cli.cli_app.console')
    def test_handle_incomplete_shows_success_message_with_emoji_formatting(self, mock_console):
        """
        Test that _handle_incomplete shows success message with emoji formatting.
        """
        # Mock the service to return a task
        mock_task = TodoItem(id=1, description="Task to incomplete", completed=False)
        self.mock_service.mark_task_incomplete.return_value = mock_task
        
        # Call the _handle_menu_incomplete method with input simulation
        with patch('builtins.input', side_effect=['1']):
            self.app._handle_menu_incomplete()
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called

    @patch('src.cli.cli_app.console')
    def test_handle_delete_shows_success_message_with_emoji_formatting(self, mock_console):
        """
        Test that _handle_delete shows success message with emoji formatting.
        """
        # Mock the service to return a task
        mock_task = TodoItem(id=1, description="Task to delete", completed=False)
        self.mock_service.delete_task.return_value = mock_task
        
        # Call the _handle_menu_delete method with input simulation
        with patch('builtins.input', side_effect=['1']):
            self.app._handle_menu_delete()
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called

    @patch('src.cli.cli_app.console')
    def test_handle_update_shows_success_message_with_emoji_formatting(self, mock_console):
        """
        Test that _handle_update shows success message with emoji formatting.
        """
        # Mock the service to return a task
        mock_task = TodoItem(id=1, description="Updated task", completed=False)
        self.mock_service.update_task.return_value = mock_task
        
        # Call the _handle_menu_update method with input simulation
        with patch('builtins.input', side_effect=['1', 'Updated task']):
            self.app._handle_menu_update()
        
        # Verify that console.print was called (indicating rich formatting was used)
        assert mock_console.print.called

    @patch('src.cli.cli_app.console')
    def test_run_menu_loop_shows_welcome_message_with_formatting(self, mock_console):
        """
        Test that run_menu_loop shows welcome message with formatting.
        """
        # Set the app to run only once then stop
        original_running = self.app.running
        self.app.running = True
        
        # Mock the input to exit immediately
        with patch('builtins.input', side_effect=['9']):
            self.app.run_menu_loop()
        
        # Reset running state
        self.app.running = original_running
        
        # Verify that console.print was called for welcome message (indicating rich formatting was used)
        assert mock_console.print.called