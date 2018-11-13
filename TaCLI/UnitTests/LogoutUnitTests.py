from unittest import TestCase
from TaCLI.Components.Logout import Logout
from TaCLI.TextFileInterface import TextFileInterface
from TaCLI.Environment import Environment
from TaCLI.User import User


class LogoutUnitTests(TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_successful_logout(self):
        self.environment.user = User("root", "administrator")
        logout = Logout(self.environment)
        response = logout.action(["logout"])

        self.assertEqual(response, "Logged out.")
        self.assertIsNone(self.environment.user)

    def test_not_logged_on(self):
        logout = Logout(self.environment)
        response = logout.action(["logout"])

        self.assertEqual(response, "Error logging out.")
        self.assertIsNone(self.environment.user)

    def test_extra_args(self):
        self.environment.user = User("root", "administrator")
        logout = Logout(self.environment)
        response = logout.action(["logout", "foo"])

        self.assertEqual(response, "Error logging out.")
        self.assertIsNotNone(self.environment.user)
