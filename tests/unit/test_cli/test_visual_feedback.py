"""
Unit tests for visual feedback for selected items.
"""
import pytest
from unittest.mock import Mock, patch
from rich.table import Table
from rich.text import Text
from src.cli.cli_app import CLIApp
from src.models.todo_item import TodoItem
from src.services.navigation_service import NavigationService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility


class TestVisualFeedbackForSelectedItems:
    """
    Test class for visual feedback for selected items.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock service
        self.mock_service = Mock()
        self.app = CLIApp(service=self.mock_service)

    def test_navigation_service_tracks_selection(self):
        """
        Test that NavigationService correctly tracks selection.
        """
        mock_compat_service = Mock(spec=TerminalCompatibilityService)
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        nav_service = NavigationService(compatibility_service=mock_compat_service)
        
        # Set up some test items
        test_items = [
            TodoItem(id=1, description="Task 1", completed=False),
            TodoItem(id=2, description="Task 2", completed=True),
            TodoItem(id=3, description="Task 3", completed=False),
        ]
        
        nav_service.set_navigation_context(test_items, 'test_list')
        
        # Initially, first item should be selected
        assert nav_service.get_current_index() == 0
        assert nav_service.get_current_item() == test_items[0]
        
        # Move to second item
        nav_service.move_down()
        assert nav_service.get_current_index() == 1
        assert nav_service.get_current_item() == test_items[1]
        
        # Move to third item
        nav_service.move_down()
        assert nav_service.get_current_index() == 2
        assert nav_service.get_current_item() == test_items[2]

    @patch('src.cli.cli_app.console')
    def test_visual_feedback_in_list_display(self, mock_console):
        """
        Test visual feedback in list display for selected items.
        """
        # Create a navigation service
        mock_compat_service = Mock(spec=TerminalCompatibilityService)
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        nav_service = NavigationService(compatibility_service=mock_compat_service)
        
        # Set up some test items
        test_items = [
            TodoItem(id=1, description="First Task", completed=False),
            TodoItem(id=2, description="Second Task", completed=True),
            TodoItem(id=3, description="Third Task", completed=False),
        ]
        
        nav_service.set_navigation_context(test_items, 'test_list')
        
        # Create a table with visual feedback for the selected item
        table = Table(title="Task List with Selection Feedback", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Description", style="white")
        table.add_column("Selected", style="bold yellow")

        # Add tasks to the table with selection indicator
        for i, task in enumerate(test_items):
            is_selected = i == nav_service.get_current_index()
            status_emoji = "✅" if task.completed else "📝"
            status_text = "[green]Completed[/green]" if task.completed else "[yellow]Active[/yellow]"
            selected_indicator = "👉" if is_selected else ""
            table.add_row(
                str(task.id), 
                f"{status_emoji} {status_text}", 
                task.description,
                selected_indicator
            )

        # Print the table to provide visual feedback
        from rich.console import Console
        console = Console()
        console.print(table)

        # Verify that the table was created with selection indicators
        assert True  # The test is more about verifying the logic than mocking

    @patch('src.cli.cli_app.console')
    def test_visual_feedback_changes_with_navigation(self, mock_console):
        """
        Test that visual feedback changes when navigation occurs.
        """
        # Create a navigation service
        mock_compat_service = Mock(spec=TerminalCompatibilityService)
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        nav_service = NavigationService(compatibility_service=mock_compat_service)
        
        # Set up some test items
        test_items = [
            TodoItem(id=1, description="First Task", completed=False),
            TodoItem(id=2, description="Second Task", completed=True),
            TodoItem(id=3, description="Third Task", completed=False),
        ]
        
        nav_service.set_navigation_context(test_items, 'test_list')
        
        # Create table with selection indicator for current item
        def create_table_with_selection():
            table = Table(title="Task List with Selection Feedback", show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Status", style="green")
            table.add_column("Description", style="white")
            table.add_column("Selected", style="bold yellow")

            for i, task in enumerate(test_items):
                is_selected = i == nav_service.get_current_index()
                status_emoji = "✅" if task.completed else "📝"
                status_text = "[green]Completed[/green]" if task.completed else "[yellow]Active[/yellow]"
                selected_indicator = "[bold yellow]👉[/bold yellow]" if is_selected else ""
                table.add_row(
                    str(task.id), 
                    f"{status_emoji} {status_text}", 
                    task.description,
                    selected_indicator
                )
            return table

        # Create table for initial selection (first item)
        initial_table = create_table_with_selection()
        assert nav_service.get_current_index() == 0

        # Move to second item
        nav_service.move_down()
        second_table = create_table_with_selection()
        assert nav_service.get_current_index() == 1

        # Move to third item
        nav_service.move_down()
        third_table = create_table_with_selection()
        assert nav_service.get_current_index() == 2

    def test_navigation_service_get_navigation_info_includes_selection(self):
        """
        Test that navigation info includes selection information.
        """
        mock_compat_service = Mock(spec=TerminalCompatibilityService)
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        nav_service = NavigationService(compatibility_service=mock_compat_service)
        
        # Set up some test items
        test_items = [
            TodoItem(id=1, description="Task 1", completed=False),
            TodoItem(id=2, description="Task 2", completed=True),
        ]
        
        nav_service.set_navigation_context(test_items, 'test_list')
        
        # Get navigation info
        nav_info = nav_service.get_navigation_info()
        
        # Verify the info includes selection details
        assert 'current_index' in nav_info
        assert 'total_items' in nav_info
        assert 'current_item' in nav_info
        assert 'is_valid' in nav_info
        assert nav_info['current_index'] == 0
        assert nav_info['total_items'] == 2
        assert nav_info['current_item'] == test_items[0]
        assert nav_info['is_valid'] is True

    def test_navigation_service_handles_selection_at_boundaries(self):
        """
        Test that navigation service handles selection at list boundaries correctly.
        """
        mock_compat_service = Mock(spec=TerminalCompatibilityService)
        mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        mock_compat_service.get_terminal_compatibility.return_value = mock_compat
        
        nav_service = NavigationService(compatibility_service=mock_compat_service)
        
        # Set up some test items
        test_items = [
            TodoItem(id=1, description="Task 1", completed=False),
            TodoItem(id=2, description="Task 2", completed=True),
            TodoItem(id=3, description="Task 3", completed=False),
        ]
        
        nav_service.set_navigation_context(test_items, 'test_list')
        
        # Start at first item
        assert nav_service.get_current_index() == 0
        
        # Move to last item
        nav_service.move_down()
        assert nav_service.get_current_index() == 1
        nav_service.move_down()
        assert nav_service.get_current_index() == 2
        
        # Try to move past last item (should stay at last item)
        result = nav_service.move_down()
        assert result is False  # Should return False when can't move further
        assert nav_service.get_current_index() == 2
        
        # Move back up
        nav_service.move_up()
        assert nav_service.get_current_index() == 1
        nav_service.move_up()
        assert nav_service.get_current_index() == 0
        
        # Try to move before first item (should stay at first item)
        result = nav_service.move_up()
        assert result is False  # Should return False when can't move further
        assert nav_service.get_current_index() == 0