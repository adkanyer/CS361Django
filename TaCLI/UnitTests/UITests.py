from unittest import TestCase
from TaCLI.UI import UI
from TaCLI.TextFileInterface import TextFileInterface
from TaCLI.Environment import Environment


class CommandTests(TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.ui = UI(self.environment)
        self.environment.database.clear_database()

    def test_parse_commands(self):
        self.assertTrue(self.ui.parse_commands("command1 command2 command3"),
                        {"command1", "command2", "command2"})

    def test_command(self):
        self.assertEqual(self.ui.command("invalid_arg arg arg arg"), "Invalid Command")

    def test_valid_command(self):
        self.assertEqual(self.ui.command("assign_lab 361 801 appoorv"), "ERROR")
