from django.test import TestCase
from TaCLI import UI, Environment
from TaApp.DjangoModelInterface import DjangoModelInterface

class DeleteAccountTest(TestCase):
    def setUp(self):
        """
            create dummy account for each of the types of users:
            supervisor, administrator, instructor and TA and then
            log them in for their respected tests
            Each test is implemented by first creating and then deleting an account
        """
        self.di = DjangoModelInterface()

        self.di.create_account("Supervisor", "SupervisorPassword", "supervisor")
        self.di.create_account("Administrator", "AdministratorPassword", "administrator")
        self.di.create_account("Instructor", "InstructorPassword", "instructor")
        self.di.create_account("TA", "TAPassword", "TA")

        self.di.create_course("361", "CompSci361")
        self.di.create_lab("361", "801")

        self.environment = Environment.Environment(self.di, DEBUG=True)
        self.ui = UI.UI(self.environment)

        """
            The supervisor and administrator are able to delete accounts
            when delete_account command is entered, it expects 1 arguments:
            - username
            The response is a string of either:
            - "Account Deleted" if successful
            - "Unable to delete account" if unsuccessful
        """

    def test_command_delete_account_supervisor(self):

        # login as supervisor
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.ui.command("create_account", ["create_account", "john", "password", "TA"])
        self.assertEqual(self.ui.command("delete_account", {"user": "john"}), "Account deleted.")

    def test_command_delete_account_administrator(self):

        # login as administrator
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        self.ui.command("create_account", ["create_account", "adam", "password", "supervisor"])
        self.assertEqual(self.ui.command("delete_account", {"user": "adam"}), "Account deleted.")

    def test_command_delete_account_instructor(self):

        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        self.ui.command("create_account", ["create_account", "aaron", "password", "supervisor"])
        self.ui.command("logout", "")

        # login as instructor
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        # instructor cannot delete accounts
        self.assertEqual(self.ui.command("delete_account", {"user": "aaron"}), "ERROR")

    def test_command_delete_account_TA(self):
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.ui.command("create_account", ["create_account", "tim", "password", "TA"])
        self.ui.command("logout", "")

        # login as TA
        self.ui.command("login", {"username": "TA", "password": "TAPassword"})
        # TA cannot delete accounts
        self.assertEqual(self.ui.command("delete_account", {"user": "tim"}), "ERROR")

    def test_command_delete_account_format(self):
        # login as administrator
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        # not enough arguments
        self.assertEqual(self.ui.command("delete_account", {}), "ERROR")

    def test_command_delete_account_nonexisting(self):
        # login as supervisor
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("delete_account", {"user": ""}), "ERROR")
