import unittest


class EditAccountTest(unittest.TestCase):
    def setUp(self):
        self.ui = UI()
        """
            create dummy account for each of the types of users:
            supervisor, administrator, instructor and TA and then
            log them in for their respected tests
        """
        self.ui.command("create_account userSupervisor password supervisor")
        self.ui.command("create_account userAdministrator password administrator")
        self.ui.command("create_account userInstructor password instructor")
        self.ui.command("create_account userTA password ta")

        """
            The supervisor and administrator are able to edit accounts
            when edit_account command is entered, it expects 2 arguments:
            - username
            - new password
            The response is a string of either:
            - "Password Changed" if successful
            - "Unable to change password" if unsuccessful
    """

    def test_command_edit_account_supervisor(self):

        # login and create an account supervisor
        self.ui.command("login userSupervisor password")
        self.ui.command("create_account user password TA")

        self.assertEquals("edit_account user password1", "Password Changed")

    def test_command_edit_account_administrator(self):

        # login as administrator
        self.ui.command("login userAdministrator password")
        self.ui.command("create_account user1 password supervisor")

        self.assertEquals("edit_account user1 password1", "Password Changed")

    def test_command_edit_account_instructor(self):
        self.ui.command("login userSupervisor password")
        self.ui.command("create_account tim@uwm.edu tim password")
        self.ui.command("logout")

        # login as instructor
        self.ui.command("login userInstructor password")
        # instructor cannot create accounts
        self.assertEquals("edit_account tim password1", "Unable to change password")

    def test_command_edit_account_TA(self):
        self.ui.command("login userSupervisor password")
        self.ui.command("create_account tim password TA")
        self.ui.command("logout")

        # login as TA
        self.ui.command("login userTA password")
        # TA cannot create accounts
        self.assertEquals("edit_account tim password1", "Unable to change password")

    def test_command_edit_account_format(self):
        # login as administrator
        self.ui.command("login userAdministrator password")

        self.assertEquals("edit_account", "Unable to change password")

    def test_command_edit_account_nonexisting(self):
        # login as supervisor
        self.ui.command("login userSupervisor password")

        self.assertEquals("edit_account noUser password1", "Unable to change password")
