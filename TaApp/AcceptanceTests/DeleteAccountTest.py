import unittest
import UI, Environment
import TextFileInterface


class DeleteAccountTest(unittest.TestCase):
    def setUp(self):
        """
            create dummy account for each of the types of users:
            supervisor, administrator, instructor and TA and then
            log them in for their respected tests
            Each test is implemented by first creating and then deleting an account
        """
        tfi = TextFileInterface.TextFileInterface(relative_directory="../UnitTests/TestDB/")
        tfi.clear_database()

        tfi.create_account("userSupervisor", "password", "supervisor")
        tfi.create_account("userAdministrator", "password", "administrator")
        tfi.create_account("userInstructor", "password", "instructor")
        tfi.create_account("userTA", "password", "TA")

        tfi.create_course("361", "CompSci361")
        tfi.create_lab("361", "801")

        environment = Environment.Environment(tfi, DEBUG=True)
        self.ui = UI.UI(environment)

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
        self.ui.command("login userSupervisor password")
        self.ui.command("create_account john password TA")
        self.assertEqual(self.ui.command("delete_account john"), "Account deleted.")

    def test_command_delete_account_administrator(self):

        # login as administrator
        self.ui.command("login userAdministrator password")
        self.ui.command("create_account adam password supervisor")
        self.assertEqual(self.ui.command("delete_account adam"), "Account deleted.")

    def test_command_delete_account_instructor(self):

        self.ui.command("login userAdministrator password")
        self.ui.command("create_account aaron password supervisor")
        self.ui.command("logout")

        # login as instructor
        self.ui.command("login userInstructor password")
        # instructor cannot delete accounts
        self.assertEqual(self.ui.command("delete_account aaron"), "Error deleting account.")

    def test_command_delete_account_TA(self):
        self.ui.command("login userSupervisor password")
        self.ui.command("create_account tim password TA")
        self.ui.command("logout")

        # login as TA
        self.ui.command("login userTA password")
        # TA cannot delete accounts
        self.assertEqual(self.ui.command("delete_account tim"), "Error deleting account.")

    def test_command_delete_account_format(self):
        # login as administrator
        self.ui.command("login userAdministrator password")
        # not enough arguments
        self.assertEqual(self.ui.command("delete_account"), "Error deleting account.")

    def test_command_delete_account_nonexisting(self):
        # login as supervisor
        self.ui.command("login userSupervisor password")
        self.assertEqual(self.ui.command("delete_account noUser"), "Error deleting account.")
