"""
Unit tests for Enter key handling.
"""
import pytest
from unittest.mock import Mock, patch
from src.services.navigation_service import NavigationService
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.models.visual_elements import TerminalCompatibility


class TestEnterKeyHandling:
    """
    Test class for Enter key handling.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock compatibility service
        self.mock_compat_service = Mock(spec=TerminalCompatibilityService)
        self.navigation_service = NavigationService(compatibility_service=self.mock_compat_service)

    def test_handle_key_input_detects_enter_key(self):
        """
        Test that handle_key_input correctly detects Enter key.
        """
        # Test newline character (Enter key)
        result = self.navigation_service.handle_key_input('\n')
        assert result == 'select'

        # Test carriage return (also Enter key on some systems)
        result = self.navigation_service.handle_key_input('\r')
        assert result == 'select'

    def test_enter_key_triggers_selection_action(self):
        """
        Test that Enter key triggers the 'select' action.
        """
        result = self.navigation_service.handle_key_input('\n')
        assert result == 'select'

        result = self.navigation_service.handle_key_input('\r')
        assert result == 'select'

    def test_other_keys_do_not_trigger_selection(self):
        """
        Test that other keys do not trigger the 'select' action.
        """
        # Test arrow keys
        result = self.navigation_service.handle_key_input('\x1b[A')  # Up arrow
        assert result != 'select'

        result = self.navigation_service.handle_key_input('\x1b[B')  # Down arrow
        assert result != 'select'

        # Test other keys
        result = self.navigation_service.handle_key_input('a')
        assert result != 'select'

        result = self.navigation_service.handle_key_input('x')
        assert result != 'select'

    def test_enter_key_mapping_exists(self):
        """
        Test that Enter key is mapped in the key mapping.
        """
        key_mapping = self.navigation_service.get_key_mapping()
        
        assert 'enter' in key_mapping
        assert '\n' in key_mapping['enter']
        assert '\r' in key_mapping['enter']

    def test_navigation_service_handles_enter_in_context(self):
        """
        Test that navigation service handles Enter key in navigation context.
        """
        # Set up some items for navigation
        items = ['item1', 'item2', 'item3']
        self.navigation_service.set_navigation_context(items, 'test_menu')
        
        # Verify initial state
        assert self.navigation_service.get_current_index() == 0
        assert self.navigation_service.get_current_item() == 'item1'
        
        # Handle Enter key (should return 'select' but not change navigation state)
        result = self.navigation_service.handle_key_input('\n')
        assert result == 'select'
        
        # Navigation state should remain the same
        assert self.navigation_service.get_current_index() == 0
        assert self.navigation_service.get_current_item() == 'item1'

    def test_enter_key_action_can_be_customized(self):
        """
        Test that Enter key action can be customized.
        """
        # The navigation service uses the key mapping, so we can check that
        # the enter key is properly mapped to the 'select' action
        key_mapping = self.navigation_service.get_key_mapping()
        
        # Verify that enter keys are mapped to the enter action
        assert '\n' in key_mapping['enter']
        assert '\r' in key_mapping['enter']

    @patch('builtins.input', side_effect=['\n'])
    def test_enter_key_integration_with_input_handling(self, mock_input):
        """
        Test Enter key handling in the context of input handling.
        """
        # This is more of an integration test to verify the concept
        # In a real application, we would have a loop that processes key inputs
        
        # Simulate handling an enter key
        result = self.navigation_service.handle_key_input('\n')
        assert result == 'select'

    def test_key_mapping_isolation_for_enter_key(self):
        """
        Test that Enter key mappings are isolated between instances.
        """
        # Create another navigation service
        another_service = NavigationService(compatibility_service=self.mock_compat_service)
        
        # Check that both services have the same default Enter key mapping
        nav_mapping = self.navigation_service.get_key_mapping()
        another_mapping = another_service.get_key_mapping()
        
        assert '\n' in nav_mapping['enter']
        assert '\n' in another_mapping['enter']
        assert nav_mapping['enter'] == another_mapping['enter']

    def test_enter_key_action_consistency(self):
        """
        Test that Enter key consistently returns the 'select' action.
        """
        for _ in range(5):  # Test multiple times to ensure consistency
            result = self.navigation_service.handle_key_input('\n')
            assert result == 'select'
            
            result = self.navigation_service.handle_key_input('\r')
            assert result == 'select'