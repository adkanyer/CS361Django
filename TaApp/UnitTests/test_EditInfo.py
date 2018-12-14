from django.test import TestCase

from TaApp.DjangoModelInterface import DjangoModelInterface
from TaCLI.Components.EditInfo import EditInfo
from TaCLI.Environment import Environment
from TaCLI.User import User


class EditInfoUnitTests(TestCase):

    def setUp(self):
        di = DjangoModelInterface()
        self.environment = Environment(di, DEBUG=True)
        self.environment.user = User("root", "administrator")

    def test_edit_info_wrong_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action({"command": "edit_info", "field": ""})
        self.assertEqual(response, "ERROR")

    def test_edit_info_phone_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action({"command" : "edit_info", "field": "phone", "phone": "1234567"})
        self.assertEqual(response, "Phone Number has been updated successfully")

    def test_edit_info_address_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action({"command": "edit_info", "field": "address", "address": "1234 Street City, State 53202"})
        self.assertEqual("Address has been updated successfully.", response)

    def test_edit_info_email_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action({"command": "edit_info", "field": "email", "email" : "john3885@uwm.edu"})
        self.assertEqual("Email has been updated successfully.", response)

    def test_edit_info_office_hours_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action({"command": "edit_info", "field": "office_hours", "time": "MW 10-12"})
        self.assertEqual("Office Hours have been updated successfully.", response)

    def test_edit_info_name_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action({"command": "edit_info", "field": "name", "first": "adsf", "last": "Johnson"})
        self.assertEqual(response, "Name has been updated successfully.")

    def test_edit_account_not_logged_in(self):
        self.environment.user = None
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info", "name", "MW", "10-12"])
        self.assertEqual(response, "ERROR")