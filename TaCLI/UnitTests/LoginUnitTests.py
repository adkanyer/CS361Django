from unittest import TestCase
from TaCLI.Components.Login import Login, Logout
from TaCLI.TextFileInterface import TextFileInterface
from TaCLI.Environment import Environment
from TaCLI.User import User


class LoginUnitTests(TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_not_enough_args(self):
        login = Login(self.environment)
        response = login.action({"username": "testuser", "password": None})

        self.assertEqual(response, "Error logging in.")
        self.assertIsNone(self.environment.user)

    def test_too_many_args(self):
        login = Login(self.environment)
        response = login.action({"username": "testuser", "password": "1234"})

        self.assertEqual(response, "Error logging in.")
        self.assertIsNone(self.environment.user)

    def test_already_logged_in(self):
        self.environment.user = User("someone_else", "supervisor")

        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        response = login.action({"username": "testuser", "password": "1234"})

        self.assertEqual(response, "Error logging in.")
        self.assertIsNotNone(self.environment.user)

    def test_wrong_username(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        response = login.action({"username": "testuse", "password": "1234"})

        self.assertEqual(response, "Error logging in.")
        self.assertIsNone(self.environment.user)

    def test_wrong_password(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        response = login.action({"username": "testuser", "password": "4321"})

        self.assertEqual(response, "Error logging in.")
        self.assertIsNone(self.environment.user)

    def test_wrong_both(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        response = login.action({"username": "testuse", "password": "4321"})

        self.assertEqual(response, "Error logging in.")
        self.assertIsNone(self.environment.user)

    def test_all_correct(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        response = login.action({"username": "testuser", "password": "1234"})

        self.assertEqual(response, "Logged in.")
        self.assertIsNotNone(self.environment.user)


class LogoutUnitTests(TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_successful_logout(self):
        self.environment.user = User("root", "administrator")
        logout = Logout(self.environment)
        response = logout.action({})

        self.assertEqual(response, "Logged out.")
        self.assertIsNone(self.environment.user)

    def test_not_logged_on(self):
        logout = Logout(self.environment)
        response = logout.action({})

        self.assertEqual(response, "Error logging out.")
        self.assertIsNone(self.environment.user)

    def test_extra_args(self):
        self.environment.user = User("root", "administrator")
        logout = Logout(self.environment)
        response = logout.action({"NotARealTHing": "nothing"})

        self.assertEqual(response, "Logged out.")
        self.assertIsNone(self.environment.user)
