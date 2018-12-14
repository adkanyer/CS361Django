import unittest
import UI, Environment
import TextFileInterface


class LoginTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface.TextFileInterface(relative_directory="../UnitTests/TestDB/")
        tfi.clear_database()

        tfi.create_account("Instructor", "InstructorPassword", "instructor")

        environment = Environment.Environment(tfi, DEBUG=True)
        self.ui = UI.UI(environment)

    """
        When the login command is entered, it takes two arguments:
        - Username
        - Password
        If the username and password match a database entry, login is a success:
        - "Logged in."
        If they do not match or are omitted, failure:
        - "Error logging in."
    """
    def test_command_login_correct(self):
        self.assertEqual(self.ui.command("login Instructor InstructorPassword"), "Logged in.")

    def test_command_login_no_pass(self):
        self.assertEqual(self.ui.command("login Instructor"), "Error logging in.")

    def test_command_login_no_args(self):
        self.assertEqual(self.ui.command("login"), "Error logging in.")

    def test_command_login_already_logged_in(self):
        self.ui.command("login Instructor InstructorPassword")
        self.assertEqual(self.ui.command("login Instructor InstructorPassword"), "Error logging in.")

    """ 
        When logout command is entered, it takes no arguments.
        It logs a user out only if there is one logged in.
        - Success: "Logged out."
        - Failure: "Error logging out."
    """
    def test_command_logout_correct(self):
        self.ui.command("login Instructor InstructorPassword")
        self.assertEqual(self.ui.command("logout"), "Logged out.")

    def test_command_logout_not_logged_in(self):
        self.assertEqual(self.ui.command("logout"), "Error logging out.")
