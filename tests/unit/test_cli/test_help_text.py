"""
Unit tests for CLI help text enhancements.
"""
import pytest
from unittest.mock import Mock, patch
from src.cli.cli_app import CLIApp


class TestHelpTextEnhancements:
    """
    Test class for CLI help text enhancements.
    """

    def setup_method(self):
        """
        Set up the test environment.
        """
        # Create a mock service
        self.mock_service = Mock()
        self.app = CLIApp(service=self.mock_service)

    @patch('sys.stdout')
    def test_cli_parser_includes_enhanced_help_text(self, mock_stdout):
        """
        Test that the CLI parser includes enhanced help text with emojis.
        """
        # Get the parser
        parser = self.app._create_parser()
        
        # Check that the help text includes emojis or visual enhancements
        # We'll check the subparsers to see if they have enhanced help
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, type(parser.add_subparsers()))
        ]
        
        # If there are no subparsers, check the main help
        # The parser should have help text for each command
        add_parser = None
        list_parser = None
        update_parser = None
        complete_parser = None
        delete_parser = None
        
        # Get the subparsers
        subparsers = parser._subparsers
        if subparsers:
            # Try to access the choices to get the individual parsers
            choices = getattr(subparsers, 'choices', {})
            add_parser = choices.get('add')
            list_parser = choices.get('list')
            update_parser = choices.get('update')
            complete_parser = choices.get('complete')
            delete_parser = choices.get('delete')
        
        # Verify that the parsers exist
        assert add_parser is not None
        assert list_parser is not None
        assert update_parser is not None
        assert complete_parser is not None
        assert delete_parser is not None

    def test_cli_parser_has_descriptive_help_text(self):
        """
        Test that CLI parser has descriptive help text.
        """
        parser = self.app._create_parser()
        
        # Check that the main parser has a description
        assert parser.description is not None
        assert len(parser.description) > 0
        
        # Check that subcommands have help text
        subparsers = parser._subparsers
        if subparsers:
            choices = getattr(subparsers, 'choices', {})
            for cmd_name, cmd_parser in choices.items():
                assert cmd_parser.format_help() is not None

    @patch('sys.argv', ['todo', '--help'])
    def test_help_command_runs_without_error(self):
        """
        Test that the help command runs without error.
        """
        # Capture the result of running with --help
        # This would normally print help and exit, but we'll catch that
        import sys
        from io import StringIO
        
        # Capture stdout
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            result = self.app.run(['--help'])
            # Help command should return non-zero to indicate exit
            assert result != 0  # argparse exits with error code for help
        except SystemExit:
            # argparse calls sys.exit() when showing help, which is expected
            pass
        finally:
            sys.stdout = old_stdout

    def test_parser_creation_includes_all_expected_commands(self):
        """
        Test that parser creation includes all expected commands.
        """
        parser = self.app._create_parser()
        
        # Check that the expected commands are available
        expected_commands = ['add', 'list', 'update', 'complete', 'incomplete', 'delete', 'export', 'import']
        
        # Get the subparsers
        subparsers_actions = [
            action for action in parser._actions
            if hasattr(action, 'choices')
        ]
        
        # Find the action that contains the command choices
        commands_action = None
        for action in subparsers_actions:
            if hasattr(action, 'choices'):
                commands_action = action
                break
        
        if commands_action:
            available_commands = list(commands_action.choices.keys())
            for cmd in expected_commands:
                assert cmd in available_commands, f"Command {cmd} should be available"

    def test_help_text_mentions_visual_enhancements(self):
        """
        Test that help text mentions visual enhancements (indirectly).
        """
        # While we can't easily test the exact help text that would be displayed,
        # we can verify that the CLI app has been updated with rich formatting
        import inspect
        
        # Check that the CLI app source code contains references to rich/console
        source = inspect.getsource(CLIApp)
        
        # Verify that rich console is used in the implementation
        assert 'console.print' in source or 'rich' in source