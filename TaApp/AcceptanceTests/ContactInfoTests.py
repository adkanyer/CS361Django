import unittest
import TextFileInterface
import Environment
import UI


class ContactInfoTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface.TextFileInterface(relative_directory="../UnitTests/TestDB/")
        tfi.clear_database()
        environment = Environment.Environment(tfi)
        self.ui = UI.UI(environment)

    def test_command_view_public_info(self):
        """
            Only public information is available for a normal user to see. Only those with permission can view
            private information like address and phone number.

            When view_info command is entered for a user you only have public access to, it expects one argument:
            - username

            The response is a string:
            - If successful: "username role"
            - If failure: "Username does not exist"
        """
        # Create a TA account and log in as part of the setup
        self.ui.command("create_account userTA userPassword TA")
        self.ui.command("login userTA userPassword")

        # view own contact info, expect success
        self.assertEquals(self.ui.command("view_info"), "erin erinfink@uwm.edu\n"
                                                        "Phone number: 1231231234,"
                                                        "Address: 2311 E Hartford Ave Milwaukee, WI 53211")
        # Command: "view_info user", expect success
        self.assertEquals(self.ui.command("view_info Erin"), "Username: erin, Email: erinfink@uwm.edu")

        # Command: "view_info fake", expect success
        self.assertEquals(self.ui.command("view_info fake"), "Username does not exist.")

    def test_command_Instructor_change_contact_info_valid(self):
        self.ui.command("login userInstructor password")

        # Instructor changes own email, phone number, password; expected success
        self.assertEquals(self.ui.command("edit_contact email: erincfink@uwm.edu"), "Email has been updated.")
        self.assertEquals(self.ui.command("edit_contact phone: 1234123443"), "Phone has been updated.")
        self.assertEquals(self.ui.command("edit_contact address: 1234 Sesame St Milwaukee, WI 12312"),
                          "Address has been updated.")

    def test_command_TA_change_contact_info(self):
        self.ui.command("login userTA password")

        # Ta changes own info
        self.assertEquals(self.ui.command("edit_contact email: erincfink@uwm.edu"), "Email has been updated.")
        self.assertEquals(self.ui.command("edit_contact phone: 1234123443"), "Phone has been updated.")
        self.assertEquals(self.ui.command("edit_contact address: 1234 Sesame St Milwaukee, WI 12312"),
                          "Address has been updated.")

    def test_command_edit_contact_format(self):
        self.ui.command("login userInstructor password")

        # no argument given
        self.assertEquals(self.ui.command("edit_contact"), "Unable to change contact information")



