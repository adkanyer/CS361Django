from django.test import TestCase
from TaCLI import UI, Environment
from TaApp.DjangoModelInterface import DjangoModelInterface


class CreateAccountTest(TestCase):
    def setUp(self):
        """
            create dummy account for each of the types of users:
            supervisor, administrator, instructor and TA and then
            log them in for their respected tests
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
            The supervisor and administrator are able to create accounts
            when create_account command is entered, it expects 3 arguments:
            - email
            - username
            - password
            The response is a string of either:
            - "Account created." if successful
            - "Error creating account." if unsuccessful
    """

    def test_command_create_account_supervisor(self):

        # login as supervisor
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("create_account", ["create_account", "john", "password", "TA"]), "Account created.")

    def test_command_create_account_administrator(self):

        # login as administrator
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        self.assertEqual(self.ui.command("create_account", ["create_account", "adam", "password", "supervisor"]), "Account created.")

    def test_command_create_account_instructor(self):

        # login as instructor
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        # instructor cannot create accounts
        self.assertEqual(self.ui.command("create_account", ["create_account", "aaron", "password", "instructor"]), "ERROR")

    def test_command_create_account_TA(self):

        # login as TA
        self.ui.command("login", {"username": "TA", "password": "TAPassword"})
        # TA cannot create accounts
        self.assertEqual(self.ui.command("create_account", ["create_account", "tim@uwm.edu", "tim", "password"]), "ERROR")

    def test_command_create_account_format(self):
        # login as administrator
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})

        self.assertEqual(self.ui.command("create_account", ["create_account"]), "ERROR")
        self.assertEqual(self.ui.command("create_account", ["create_account", "tyler"]), "ERROR")
        self.assertEqual(self.ui.command("create_account", ["create_account", "password"]), "ERROR")
        self.assertEqual(self.ui.command("create_account", ["create_account", "Administrator", "pass"]), "ERROR")

    def test_command_create_account_duplicate(self):
        # login as supervisor
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("create_account", ["create_account", "userTA", "password", "instructor"]), "Account created.")
        self.assertEqual(self.ui.command("create_account", ["create_account", "userTA", "password", "instructor"]), "ERROR")