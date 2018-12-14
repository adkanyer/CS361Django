from django.test import TestCase

from TaApp.DjangoModelInterface import DjangoModelInterface
from TaCLI.UI import *
from TaCLI.Environment import Environment
from TaCLI.User import User


class CommandTests(TestCase):
    def setUp(self):
        di = DjangoModelInterface()
        self.environment = Environment(di, DEBUG=True)
        self.ui = UI(self.environment)

    def test_parse_commands(self):
        self.assertTrue(self.ui.parse_commands("command1 command2 command3"),
                        {"command1", "command2", "command2"})

    def test_command(self):
        self.assertEqual(self.ui.command(command="invalid", args="arg arg arg"), "Invalid Command")

    def test_valid_command(self):
        self.assertEqual(self.ui.command(command="assign_lab", args="361 801 appoorv"), "ERROR")