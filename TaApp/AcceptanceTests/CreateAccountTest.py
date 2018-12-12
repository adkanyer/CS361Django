import unittest
import UI, Environment
import TextFileInterface


class CreateAccountTest(unittest.TestCase):
    def setUp(self):
        """
            create dummy account for each of the types of users:
            supervisor, administrator, instructor and TA and then
            log them in for their respected tests
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
        self.ui.command("login userSupervisor password")
        self.assertEqual(self.ui.command("create_account john password TA"), "Account created.")

    def test_command_create_account_administrator(self):

        # login as administrator
        self.ui.command("login userAdministrator password")
        self.assertEqual(self.ui.command("create_account adam password supervisor"), "Account created.")

    def test_command_create_account_instructor(self):

        # login as instructor
        self.ui.command("login userInstructor password")
        # instructor cannot create accounts
        self.assertEqual(self.ui.command("create_account aaron password instructor"), "Error creating account.")

    def test_command_create_account_TA(self):

        # login as TA
        self.ui.command("login TA password")
        # TA cannot create accounts
        self.assertEqual(self.ui.command("create_account tim@uwm.edu tim password"), "Error creating account.")

    def test_command_create_account_format(self):
        # login as administrator
        self.ui.command("login userAdministrator password")

        self.assertEqual(self.ui.command("create_account"), "Error creating account.")
        self.assertEqual(self.ui.command("create_account tyler"), "Error creating account.")
        self.assertEqual(self.ui.command("create_account james"), "Error creating account.")
        self.assertEqual(self.ui.command("create_account jim password"), "Error creating account.")

    def test_command_create_account_duplicate(self):
        # login as supervisor
        self.ui.command("login userSupervisor password")
        self.assertEqual(self.ui.command("create_account userTA password instructor"), "Error creating account.")
