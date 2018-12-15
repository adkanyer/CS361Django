from django.test import TestCase
from TaCLI import UI, Environment
from TaApp.DjangoModelInterface import DjangoModelInterface


class LoginTests(TestCase):
    def setUp(self):
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
        When the login command is entered, it takes two arguments:
        - Username
        - Password
        If the username and password match a database entry, login is a success:
        - "Logged in."
        If they do not match or are omitted, failure:
        - "Error logging in."
    """
    def test_command_login_correct_super(self):
        self.assertEqual(self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"}),
                         "Logged in.")

    def test_command_login_correct_admin(self):
        self.assertEqual(self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"}),
                         "Logged in.")

    def test_command_login_correct_instructor(self):
        self.assertEqual(self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"}),
                         "Logged in.")

    def test_command_login_no_pass(self):
        self.assertEqual(self.ui.command("login", {"username": "Instructor"}),
                         "Error logging in.")

    def test_command_login_no_args(self):
        self.assertEqual(self.ui.command("login", {}), "Error logging in.")

    def test_command_login_no_args_username(self):
        self.assertEqual(self.ui.command("login", {"username":"", "password": "InstructorPassword"}), "Error logging in.")

    def test_command_login_no_args_password(self):
        self.assertEqual(self.ui.command("login", {"username":"Instructor", "password": ""}), "Error logging in.")

    def test_command_login_already_logged_in(self):
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        self.assertEqual(self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"}),
                         "Error logging in.")

    """ 
        When logout command is entered, it takes no arguments.
        It logs a user out only if there is one logged in.
        - Success: "Logged out."
        - Failure: "Error logging out."
    """
    def test_command_logout_correct(self):
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        self.assertEqual(self.ui.command("logout", ""), "Logged out.")

    def test_command_logout_not_logged_in(self):
        self.assertEqual(self.ui.command("logout", ""), "Error logging out.")
