"""
Unit tests for keyboard input listener.
"""
import pytest
from unittest.mock import Mock, patch
import sys
import io
from src.services.navigation_service import NavigationService
from src.services.terminal_compatibility_service import TerminalCompatibilityService


class TestKeyboardInputListener:
    """
    Test class for keyboard input listener functionality.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service
        self.mock_compat_service = Mock(spec=TerminalCompatibilityService)
        self.navigation_service = NavigationService(compatibility_service=self.mock_compat_service)

    def test_handle_key_input_processes_up_arrow_correctly(self):
        """
        Test that handle_key_input processes up arrow key correctly.
        """
        result = self.navigation_service.handle_key_input('\x1b[A')  # Up arrow
        assert result == 'up'

    def test_handle_key_input_processes_down_arrow_correctly(self):
        """
        Test that handle_key_input processes down arrow key correctly.
        """
        result = self.navigation_service.handle_key_input('\x1b[B')  # Down arrow
        assert result == 'down'

    def test_handle_key_input_processes_left_arrow_correctly(self):
        """
        Test that handle_key_input processes left arrow key correctly.
        """
        result = self.navigation_service.handle_key_input('\x1b[D')  # Left arrow
        assert result == 'none'  # Left not handled by default

    def test_handle_key_input_processes_right_arrow_correctly(self):
        """
        Test that handle_key_input processes right arrow key correctly.
        """
        result = self.navigation_service.handle_key_input('\x1b[C')  # Right arrow
        assert result == 'none'  # Right not handled by default

    def test_handle_key_input_processes_enter_key_correctly(self):
        """
        Test that handle_key_input processes enter key correctly.
        """
        result = self.navigation_service.handle_key_input('\n')  # Enter
        assert result == 'select'

        result = self.navigation_service.handle_key_input('\r')  # Carriage return
        assert result == 'select'

    def test_handle_key_input_processes_exit_keys_correctly(self):
        """
        Test that handle_key_input processes exit keys correctly.
        """
        result = self.navigation_service.handle_key_input('\x1b')  # ESC
        assert result == 'exit'

        result = self.navigation_service.handle_key_input('q')
        assert result == 'exit'

        result = self.navigation_service.handle_key_input('Q')
        assert result == 'exit'

    def test_handle_key_input_processes_wasd_movement_keys_correctly(self):
        """
        Test that handle_key_input processes WASD movement keys correctly.
        """
        result = self.navigation_service.handle_key_input('w')  # Up
        assert result == 'up'

        result = self.navigation_service.handle_key_input('W')  # Up
        assert result == 'up'

        result = self.navigation_service.handle_key_input('s')  # Down
        assert result == 'down'

        result = self.navigation_service.handle_key_input('S')  # Down
        assert result == 'down'

    def test_handle_key_input_returns_none_for_unrecognized_keys(self):
        """
        Test that handle_key_input returns 'none' for unrecognized keys.
        """
        result = self.navigation_service.handle_key_input('z')
        assert result == 'none'

        result = self.navigation_service.handle_key_input('1')
        assert result == 'none'

        result = self.navigation_service.handle_key_input(' ')
        assert result == 'none'

    def test_get_key_mapping_returns_correct_mappings(self):
        """
        Test that get_key_mapping returns the correct key mappings.
        """
        mapping = self.navigation_service.get_key_mapping()
        
        assert 'up' in mapping
        assert 'down' in mapping
        assert 'enter' in mapping
        assert 'exit' in mapping
        
        # Check that up includes arrow and WASD
        assert '\x1b[A' in mapping['up']
        assert 'w' in mapping['up']
        assert 'W' in mapping['up']
        
        # Check that down includes arrow and WASD
        assert '\x1b[B' in mapping['down']
        assert 's' in mapping['down']
        assert 'S' in mapping['down']
        
        # Check that enter includes both newline and carriage return
        assert '\n' in mapping['enter']
        assert '\r' in mapping['enter']
        
        # Check that exit includes ESC and Q
        assert '\x1b' in mapping['exit']
        assert 'q' in mapping['exit']
        assert 'Q' in mapping['exit']

    def test_update_key_mapping_updates_correctly(self):
        """
        Test that update_key_mapping updates the key mapping correctly.
        """
        # Check initial mapping
        initial_mapping = self.navigation_service.get_key_mapping()
        assert 'w' in initial_mapping['up']
        
        # Update the mapping
        self.navigation_service.update_key_mapping('up', ['i', 'I'])
        
        # Check updated mapping
        updated_mapping = self.navigation_service.get_key_mapping()
        assert 'i' in updated_mapping['up']
        assert 'I' in updated_mapping['up']
        assert 'w' not in updated_mapping['up']  # Old mapping should be gone

    def test_key_mapping_isolation_between_instances(self):
        """
        Test that key mappings are isolated between different instances.
        """
        # Create another navigation service
        another_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Update key mapping for the first service
        self.navigation_service.update_key_mapping('up', ['custom_up'])
        
        # Check that the other service still has the default mapping
        default_mapping = another_service.get_key_mapping()
        assert 'w' in default_mapping['up']  # Default mapping should still be there
        assert 'custom_up' not in default_mapping['up']  # Custom mapping should not be there

    @patch('sys.stdin')
    @patch('select.select')
    def test_simulate_key_input_handling(self, mock_select, mock_stdin):
        """
        Test simulating key input handling (conceptual test).
        """
        # This is a conceptual test since actual keyboard input is complex to mock
        # We're testing the logic of key handling rather than actual input
        
        # Set up navigation context
        items = ['item1', 'item2', 'item3']
        self.navigation_service.set_navigation_context(items, 'test_menu')
        
        # Simulate handling different keys
        assert self.navigation_service.handle_key_input('\x1b[B') == 'down'  # Down arrow
        assert self.navigation_service.handle_key_input('\x1b[A') == 'up'   # Up arrow
        assert self.navigation_service.handle_key_input('\n') == 'select'    # Enter
        assert self.navigation_service.handle_key_input('\x1b') == 'exit'    # ESC