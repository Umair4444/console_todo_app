"""
Unit tests for the Navigation Service.
"""
import pytest
from unittest.mock import Mock
from src.services.navigation_service import NavigationService
from src.models.visual_elements import NavigationState, TerminalCompatibility


class TestNavigationService:
    """
    Test class for Navigation Service.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service
        self.mock_compatibility_service = Mock()
        self.service = NavigationService(self.mock_compatibility_service)

    def test_set_navigation_context_initializes_navigation_state(self):
        """
        Test that set_navigation_context initializes the navigation state correctly.
        """
        items = ['item1', 'item2', 'item3']
        menu_id = 'test_menu'
        
        self.service.set_navigation_context(items, menu_id)
        
        nav_state = self.service.get_navigation_state()
        assert nav_state is not None
        assert nav_state.current_index == 0
        assert nav_state.total_items == 3
        assert nav_state.menu_id == menu_id
        assert nav_state.last_action == "init"
        assert self.service.get_current_index() == 0

    def test_get_current_item_returns_correct_item(self):
        """
        Test that get_current_item returns the correct item based on navigation state.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        # Should return first item initially
        current_item = self.service.get_current_item()
        assert current_item == 'item1'
        
        # Move to second item
        self.service.move_down()
        current_item = self.service.get_current_item()
        assert current_item == 'item2'

    def test_get_current_item_returns_none_for_empty_list(self):
        """
        Test that get_current_item returns None for an empty list.
        """
        self.service.set_navigation_context([], 'test_menu')
        
        current_item = self.service.get_current_item()
        assert current_item is None

    def test_move_up_decreases_current_index(self):
        """
        Test that move_up decreases the current index.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        # Move to second item first
        self.service.move_down()
        assert self.service.get_current_index() == 1
        
        # Move up
        result = self.service.move_up()
        assert result is True
        assert self.service.get_current_index() == 0

    def test_move_up_returns_false_when_at_first_item(self):
        """
        Test that move_up returns False when already at the first item.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        # Already at first item
        result = self.service.move_up()
        assert result is False
        assert self.service.get_current_index() == 0

    def test_move_down_increases_current_index(self):
        """
        Test that move_down increases the current index.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        result = self.service.move_down()
        assert result is True
        assert self.service.get_current_index() == 1

    def test_move_down_returns_false_when_at_last_item(self):
        """
        Test that move_down returns False when already at the last item.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        # Move to last item
        self.service.move_down()
        self.service.move_down()
        assert self.service.get_current_index() == 2
        
        # Try to move past last item
        result = self.service.move_down()
        assert result is False
        assert self.service.get_current_index() == 2

    def test_move_to_first_moves_to_first_item(self):
        """
        Test that move_to_first moves to the first item.
        """
        items = ['item1', 'item2', 'item3', 'item4']
        self.service.set_navigation_context(items, 'test_menu')
        
        # Move to last item first
        self.service.move_down()
        self.service.move_down()
        self.service.move_down()
        assert self.service.get_current_index() == 3
        
        # Move to first
        result = self.service.move_to_first()
        assert result is True
        assert self.service.get_current_index() == 0

    def test_move_to_last_moves_to_last_item(self):
        """
        Test that move_to_last moves to the last item.
        """
        items = ['item1', 'item2', 'item3', 'item4']
        self.service.set_navigation_context(items, 'test_menu')
        
        result = self.service.move_to_last()
        assert result is True
        assert self.service.get_current_index() == 3

    def test_handle_key_input_processes_arrow_keys_correctly(self):
        """
        Test that handle_key_input processes arrow keys correctly.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        # Test down arrow
        result = self.service.handle_key_input('\x1b[B')
        assert result == 'down'
        assert self.service.get_current_index() == 1
        
        # Test up arrow
        result = self.service.handle_key_input('\x1b[A')
        assert result == 'up'
        assert self.service.get_current_index() == 0

    def test_handle_key_input_processes_enter_key_correctly(self):
        """
        Test that handle_key_input processes enter key correctly.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        result = self.service.handle_key_input('\n')
        assert result == 'select'

        result = self.service.handle_key_input('\r')
        assert result == 'select'

    def test_handle_key_input_processes_exit_key_correctly(self):
        """
        Test that handle_key_input processes exit key correctly.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        result = self.service.handle_key_input('\x1b')  # ESC
        assert result == 'exit'

        result = self.service.handle_key_input('q')
        assert result == 'exit'

    def test_handle_key_input_returns_none_for_unrecognized_key(self):
        """
        Test that handle_key_input returns 'none' for unrecognized keys.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        result = self.service.handle_key_input('z')
        assert result == 'none'

    def test_reset_navigation_resets_to_beginning(self):
        """
        Test that reset_navigation resets to the beginning.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        # Move to last item first
        self.service.move_down()
        self.service.move_down()
        assert self.service.get_current_index() == 2
        
        # Reset navigation
        self.service.reset_navigation()
        assert self.service.get_current_index() == 0

    def test_is_navigation_valid_returns_correct_value(self):
        """
        Test that is_navigation_valid returns the correct value.
        """
        # Test with valid navigation
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        assert self.service.is_navigation_valid() is True

        # Test with invalid index
        self.service.navigation_state.current_index = 5  # Beyond list length
        assert self.service.is_navigation_valid() is False

        # Test with empty list
        self.service.set_navigation_context([], 'test_menu')
        assert self.service.is_navigation_valid() is True  # Special case for empty list

    def test_get_navigation_info_returns_correct_info(self):
        """
        Test that get_navigation_info returns correct information.
        """
        items = ['item1', 'item2', 'item3']
        self.service.set_navigation_context(items, 'test_menu')
        
        info = self.service.get_navigation_info()
        assert info['current_index'] == 0
        assert info['total_items'] == 3
        assert info['menu_id'] == 'test_menu'
        assert info['last_action'] == 'init'
        assert info['is_valid'] is True
        assert info['current_item'] == 'item1'
        assert info['has_items'] is True

    def test_get_key_mapping_returns_correct_mapping(self):
        """
        Test that get_key_mapping returns the correct key mapping.
        """
        mapping = self.service.get_key_mapping()
        assert 'up' in mapping
        assert 'down' in mapping
        assert 'enter' in mapping
        assert 'exit' in mapping
        assert isinstance(mapping['up'], list)

    def test_update_key_mapping_updates_correctly(self):
        """
        Test that update_key_mapping updates the mapping correctly.
        """
        # Check initial mapping
        initial_mapping = self.service.get_key_mapping()
        assert '\x1b[A' in initial_mapping['up']
        
        # Update mapping
        self.service.update_key_mapping('up', ['k', 'K'])
        
        # Check updated mapping
        updated_mapping = self.service.get_key_mapping()
        assert 'k' in updated_mapping['up']
        assert 'K' in updated_mapping['up']
        assert '\x1b[A' not in updated_mapping['up']