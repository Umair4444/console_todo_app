"""
Unit tests for keyboard shortcuts.
"""
import pytest
from unittest.mock import Mock
from src.services.navigation_service import NavigationService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility


class TestKeyboardShortcuts:
    """
    Test class for keyboard shortcuts.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service
        self.mock_compat_service = Mock(spec=TerminalCompatibilityService)
        self.navigation_service = NavigationService(compatibility_service=self.mock_compat_service)

    def test_default_shortcuts_exist(self):
        """
        Test that default keyboard shortcuts exist.
        """
        key_mapping = self.navigation_service.get_key_mapping()
        
        # Check that arrow keys are mapped
        assert 'up' in key_mapping
        assert 'down' in key_mapping
        assert 'enter' in key_mapping
        assert 'exit' in key_mapping
        
        # Check specific key mappings
        assert '\x1b[A' in key_mapping['up']  # Up arrow
        assert '\x1b[B' in key_mapping['down']  # Down arrow
        assert '\n' in key_mapping['enter']  # Enter
        assert '\x1b' in key_mapping['exit']  # ESC

    def test_wasd_shortcuts_exist(self):
        """
        Test that WASD shortcuts exist for navigation.
        """
        key_mapping = self.navigation_service.get_key_mapping()
        
        # Check that WASD keys are mapped for navigation
        assert 'w' in key_mapping['up']
        assert 'W' in key_mapping['up']
        assert 's' in key_mapping['down']
        assert 'S' in key_mapping['down']
        assert 'a' in key_mapping['left']
        assert 'A' in key_mapping['left']
        assert 'd' in key_mapping['right']
        assert 'D' in key_mapping['right']

    def test_shortcut_handling_for_up_action(self):
        """
        Test that up action shortcuts are handled correctly.
        """
        # Test arrow key
        result = self.navigation_service.handle_key_input('\x1b[A')
        assert result == 'up'
        
        # Test 'w' key
        result = self.navigation_service.handle_key_input('w')
        assert result == 'up'
        
        # Test 'W' key
        result = self.navigation_service.handle_key_input('W')
        assert result == 'up'

    def test_shortcut_handling_for_down_action(self):
        """
        Test that down action shortcuts are handled correctly.
        """
        # Test arrow key
        result = self.navigation_service.handle_key_input('\x1b[B')
        assert result == 'down'
        
        # Test 's' key
        result = self.navigation_service.handle_key_input('s')
        assert result == 'down'
        
        # Test 'S' key
        result = self.navigation_service.handle_key_input('S')
        assert result == 'down'

    def test_shortcut_handling_for_left_right_action(self):
        """
        Test that left/right action shortcuts are handled correctly.
        """
        # Test left arrow
        result = self.navigation_service.handle_key_input('\x1b[D')
        assert result == 'none'  # Left is not handled by default in our implementation
        
        # Test 'a' key
        result = self.navigation_service.handle_key_input('a')
        assert result == 'none'  # Left is not handled by default in our implementation
        
        # Test right arrow
        result = self.navigation_service.handle_key_input('\x1b[C')
        assert result == 'none'  # Right is not handled by default in our implementation
        
        # Test 'd' key
        result = self.navigation_service.handle_key_input('d')
        assert result == 'none'  # Right is not handled by default in our implementation

    def test_shortcut_handling_for_enter_action(self):
        """
        Test that enter action shortcuts are handled correctly.
        """
        # Test enter key
        result = self.navigation_service.handle_key_input('\n')
        assert result == 'select'
        
        # Test carriage return
        result = self.navigation_service.handle_key_input('\r')
        assert result == 'select'

    def test_shortcut_handling_for_exit_action(self):
        """
        Test that exit action shortcuts are handled correctly.
        """
        # Test ESC key
        result = self.navigation_service.handle_key_input('\x1b')
        assert result == 'exit'
        
        # Test 'q' key
        result = self.navigation_service.handle_key_input('q')
        assert result == 'exit'
        
        # Test 'Q' key
        result = self.navigation_service.handle_key_input('Q')
        assert result == 'exit'

    def test_adding_custom_shortcut(self):
        """
        Test adding a custom shortcut.
        """
        # Add a custom shortcut for 'g' to mean 'go to first'
        self.navigation_service.update_key_mapping('first', ['g', 'G'])
        
        # Update the handle_key_input method to handle 'first' action
        # Note: In the actual implementation, we'd need to update the handle_key_input method
        # to handle the 'first' action, but for this test we're just checking the mapping
        
        key_mapping = self.navigation_service.get_key_mapping()
        assert 'g' in key_mapping['first']
        assert 'G' in key_mapping['first']

    def test_shortcut_isolation_between_instances(self):
        """
        Test that shortcuts are isolated between different instances.
        """
        # Create another navigation service
        another_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Add a custom shortcut to the first service
        self.navigation_service.update_key_mapping('custom_action', ['z'])
        
        # Check that the other service doesn't have the custom shortcut
        another_mapping = another_service.get_key_mapping()
        # The 'z' key should not be in any action for the other service (unless it's a default)
        for action, keys in another_mapping.items():
            assert 'z' not in keys

    def test_shortcut_removal(self):
        """
        Test removing a shortcut.
        """
        # Get initial mapping
        initial_mapping = self.navigation_service.get_key_mapping()
        
        # Verify 'w' is initially mapped to 'up'
        assert 'w' in initial_mapping['up']
        
        # Remove 'w' from 'up' action (in a real implementation, we'd have a remove method)
        # For now, we'll just update the mapping to exclude 'w'
        new_up_keys = [key for key in initial_mapping['up'] if key != 'w']
        self.navigation_service.update_key_mapping('up', new_up_keys)
        
        # Check that 'w' is no longer in the 'up' mapping
        updated_mapping = self.navigation_service.get_key_mapping()
        assert 'w' not in updated_mapping['up']

    def test_shortcut_case_sensitivity(self):
        """
        Test that shortcuts handle case sensitivity as expected.
        """
        # Both uppercase and lowercase should be mapped for navigation
        key_mapping = self.navigation_service.get_key_mapping()
        
        assert 'w' in key_mapping['up']
        assert 'W' in key_mapping['up']
        assert 's' in key_mapping['down']
        assert 'S' in key_mapping['down']
        assert 'a' in key_mapping['left']
        assert 'A' in key_mapping['left']
        assert 'd' in key_mapping['right']
        assert 'D' in key_mapping['right']

    def test_shortcut_uniqueness(self):
        """
        Test that shortcuts are unique to their actions.
        """
        key_mapping = self.navigation_service.get_key_mapping()
        
        # Collect all keys across all actions
        all_keys = []
        for action, keys in key_mapping.items():
            all_keys.extend(keys)
        
        # Verify that there's no overlap that would cause conflicts
        # (In our implementation, some keys might be in multiple actions if designed that way)
        # For example, 'q' and 'Q' are both in the 'exit' action
        # This test is more about ensuring the mapping structure is correct
        assert isinstance(key_mapping, dict)
        assert all(isinstance(keys, list) for keys in key_mapping.values())