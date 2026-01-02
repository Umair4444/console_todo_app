"""
Integration tests for arrow key navigation.
"""
import pytest
from unittest.mock import Mock, patch
from src.services.navigation_service import NavigationService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility
from src.cli.cli_app import CLIApp
from src.models.todo_item import TodoItem


class TestArrowNavigationIntegration:
    """
    Integration test class for arrow key navigation.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service
        self.mock_compat_service = Mock(spec=TerminalCompatibilityService)
        self.mock_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        self.mock_compat_service.get_terminal_compatibility.return_value = self.mock_compat

    def test_navigation_service_with_compatibility_service(self):
        """
        Test NavigationService integration with TerminalCompatibilityService.
        """
        # Create navigation service with real compatibility service
        nav_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Set up some test items
        test_items = [
            TodoItem(id=1, description="Task 1", completed=False),
            TodoItem(id=2, description="Task 2", completed=True),
            TodoItem(id=3, description="Task 3", completed=False),
        ]
        
        nav_service.set_navigation_context(test_items, 'test_list')
        
        # Verify initial state
        assert nav_service.get_current_index() == 0
        assert nav_service.get_current_item() == test_items[0]
        
        # Test navigation
        nav_service.move_down()
        assert nav_service.get_current_index() == 1
        assert nav_service.get_current_item() == test_items[1]
        
        nav_service.move_down()
        assert nav_service.get_current_index() == 2
        assert nav_service.get_current_item() == test_items[2]
        
        # Try to move past end
        result = nav_service.move_down()
        assert result is False  # Should return False when can't move further
        assert nav_service.get_current_index() == 2  # Should stay at end
        
        # Move back up
        nav_service.move_up()
        assert nav_service.get_current_index() == 1
        assert nav_service.get_current_item() == test_items[1]

    def test_key_input_handling_with_navigation(self):
        """
        Test key input handling integrated with navigation.
        """
        nav_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Set up some test items
        test_items = ["Item 1", "Item 2", "Item 3"]
        nav_service.set_navigation_context(test_items, 'test_menu')
        
        # Initially at first item
        assert nav_service.get_current_index() == 0
        assert nav_service.get_current_item() == "Item 1"
        
        # Handle down arrow key
        action = nav_service.handle_key_input('\x1b[B')
        assert action == 'down'
        
        # The navigation state should have updated
        assert nav_service.get_current_index() == 1
        assert nav_service.get_current_item() == "Item 2"
        
        # Handle up arrow key
        action = nav_service.handle_key_input('\x1b[A')
        assert action == 'up'
        
        # The navigation state should have updated
        assert nav_service.get_current_index() == 0
        assert nav_service.get_current_item() == "Item 1"

    def test_navigation_with_different_compatibility_scenarios(self):
        """
        Test navigation with different terminal compatibility scenarios.
        """
        # Test with full compatibility
        full_compat_service = Mock(spec=TerminalCompatibilityService)
        full_compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )
        full_compat_service.get_terminal_compatibility.return_value = full_compat
        
        nav_service = NavigationService(compatibility_service=full_compat_service)
        
        test_items = ["Item A", "Item B"]
        nav_service.set_navigation_context(test_items, 'test_menu')
        
        # Should work normally
        nav_service.move_down()
        assert nav_service.get_current_index() == 1
        
        # Test with limited compatibility
        limited_compat_service = Mock(spec=TerminalCompatibilityService)
        limited_compat = TerminalCompatibility(
            supports_color=False,
            supports_emoji=False,
            supports_keyboard=True,
            color_depth=32,
            encoding='utf-8'
        )
        limited_compat_service.get_terminal_compatibility.return_value = limited_compat
        
        nav_service_limited = NavigationService(compatibility_service=limited_compat_service)
        nav_service_limited.set_navigation_context(test_items, 'test_menu')
        
        # Should still work for navigation even with limited visual compatibility
        nav_service_limited.move_down()
        assert nav_service_limited.get_current_index() == 1

    @patch('src.cli.cli_app.console')
    def test_cli_integration_with_navigation_service(self, mock_console):
        """
        Test CLI integration with navigation service.
        """
        # Create a mock todo service
        mock_todo_service = Mock()
        mock_tasks = [
            TodoItem(id=1, description="CLI Task 1", completed=False),
            TodoItem(id=2, description="CLI Task 2", completed=True),
        ]
        mock_todo_service.get_all_tasks.return_value = mock_tasks
        
        cli_app = CLIApp(service=mock_todo_service)
        
        # Create navigation service with compatibility service
        nav_service = NavigationService(compatibility_service=self.mock_compat_service)
        nav_service.set_navigation_context(mock_tasks, 'cli_task_list')
        
        # Verify navigation works with the CLI context
        assert nav_service.get_current_index() == 0
        assert nav_service.get_current_item() == mock_tasks[0]
        
        nav_service.move_down()
        assert nav_service.get_current_index() == 1
        assert nav_service.get_current_item() == mock_tasks[1]

    def test_navigation_state_persistence(self):
        """
        Test that navigation state persists correctly.
        """
        nav_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Set up context
        items = ["First", "Second", "Third"]
        nav_service.set_navigation_context(items, 'persistent_test')
        
        # Navigate to middle item
        nav_service.move_down()  # Now at index 1
        assert nav_service.get_current_index() == 1
        assert nav_service.get_current_item() == "Second"
        
        # Get navigation info to verify state
        nav_info = nav_service.get_navigation_info()
        assert nav_info['current_index'] == 1
        assert nav_info['total_items'] == 3
        assert nav_info['menu_id'] == 'persistent_test'
        assert nav_info['current_item'] == "Second"
        assert nav_info['is_valid'] is True

    def test_navigation_with_empty_list(self):
        """
        Test navigation behavior with empty list.
        """
        nav_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Set up empty context
        nav_service.set_navigation_context([], 'empty_test')
        
        # Verify state for empty list
        assert nav_service.get_current_index() == -1
        assert nav_service.get_current_item() is None
        
        # Navigation actions should handle empty list gracefully
        result = nav_service.move_down()
        assert result is False  # Should return False when no items to navigate
        
        result = nav_service.move_up()
        assert result is False  # Should return False when no items to navigate

    def test_navigation_boundary_conditions(self):
        """
        Test navigation at boundary conditions.
        """
        nav_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Set up single item
        single_item = ["Only Item"]
        nav_service.set_navigation_context(single_item, 'single_test')
        
        # Should start at the only item
        assert nav_service.get_current_index() == 0
        assert nav_service.get_current_item() == "Only Item"
        
        # Moving should not change anything
        result = nav_service.move_down()
        assert result is False  # Should return False when at boundary
        assert nav_service.get_current_index() == 0  # Should stay at same position
        
        result = nav_service.move_up()
        assert result is False  # Should return False when at boundary
        assert nav_service.get_current_index() == 0  # Should stay at same position

    def test_key_mapping_integration(self):
        """
        Test that key mappings work correctly with navigation.
        """
        nav_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Set up context
        items = ["A", "B", "C"]
        nav_service.set_navigation_context(items, 'mapping_test')
        
        # Verify initial position
        assert nav_service.get_current_index() == 0
        
        # Test various key inputs
        # Down arrow
        nav_service.handle_key_input('\x1b[B')
        assert nav_service.get_current_index() == 1
        
        # 's' key (should also move down)
        nav_service.handle_key_input('s')
        assert nav_service.get_current_index() == 2
        
        # Up arrow
        nav_service.handle_key_input('\x1b[A')
        assert nav_service.get_current_index() == 1
        
        # 'w' key (should also move up)
        nav_service.handle_key_input('w')
        assert nav_service.get_current_index() == 0