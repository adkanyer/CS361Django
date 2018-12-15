from django.test import TestCase
from TaCLI import UI, Environment
from TaApp.DjangoModelInterface import DjangoModelInterface


class ContactInfoTests(TestCase):
    def setUp(self):
        self.di = DjangoModelInterface()
        self.environment = Environment.Environment(self.di, DEBUG=True)
        self.ui = UI.UI(self.environment)

    def test_command_view_private_info(self):
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
        self.di.create_account("userTA", "userPassword", "TA")
        self.ui.command("login", {"username": "userTA", "password": "userPassword"})
        self.ui.command("edit_info", {"field": "email", "email": "erin erinfink@uwm.edu"})
        self.ui.command("edit_info", {"field": "phone", "phone": "1231231234"})
        self.ui.command("edit_info", {"field": "address", "address": "Address: 2311 E Hartford Ave Milwaukee, WI 53211"})

        # view own contact info, expect success
        self.assertEquals(self.ui.command("view_info", ""), {'username': 'userTA', 'name': '', 'lname': '',
                                                             'email': 'erin erinfink@uwm.edu',
                                                             'address': 'Address: 2311 E Hartford Ave Milwaukee, WI 53211',
                                                             'phone': '1231231234', 'hours': '', 'role': 'TA'})

    def test_command_view_public_info(self):
        self.di.create_account("userTA", "userPassword", "TA")
        self.di.edit_email("userTA", "erinfink@uwm.edu")

        self.di.create_account("userInstructor", "userPassword", "instructor")
        self.ui.command("login", {"username": "userInstructor", "password": "userPassword"})

        self.assertEquals(self.ui.command("view_info", {"username": "userTA"}), {'username': 'userTA', 'name': '', 'lname': '', 'email': 'erinfink@uwm.edu', 'hours': '', 'role': 'TA'})

    def test_command_view_public_info_fake(self):
        self.di.create_account("userInstructor", "userPassword", "instructor")
        self.ui.command("login", {"username": "userInstructor", "password": "userPassword"})

        # Command: "view_info fake", expect success
        self.assertEquals(self.ui.command("view_info", {"username": "fake"}), "ERROR")

    def test_command_Instructor_change_contact_info_valid(self):
        self.di.create_account("userInstructor", "password", "instructor")
        self.ui.command("login", {"username": "userInstructor", "password": "password"})

        # Instructor changes own email, phone number, password; expected success
        self.assertEquals(self.ui.command("edit_info", {"field": "email", "email": "erin erinfink@uwm.edu"}), "Email has been updated successfully.")
        self.assertEquals(self.ui.command("edit_info", {"field": "phone", "phone": "1231231234"}), "Phone Number has been updated successfully")
        self.assertEquals(self.ui.command("edit_info",
                        {"field": "address", "address": "Address: 2311 E Hartford Ave Milwaukee, WI 53211"}),
                          "Address has been updated successfully.")

    def test_command_TA_change_contact_info(self):
        self.di.create_account("userTA", "password", "TA")
        self.ui.command("login", {"username": "userTA", "password": "password"})

        # Instructor changes own email, phone number, password; expected success
        self.assertEquals(self.ui.command("edit_info", {"field": "email", "email": "erin erinfink@uwm.edu"}),
                          "Email has been updated successfully.")
        self.assertEquals(self.ui.command("edit_info", {"field": "phone", "phone": "1231231234"}),
                          "Phone Number has been updated successfully")
        self.assertEquals(self.ui.command("edit_info",
                                          {"field": "address",
                                           "address": "Address: 2311 E Hartford Ave Milwaukee, WI 53211"}),
                          "Address has been updated successfully.")

    def test_command_Instructor_change_contact_info(self):
        self.di.create_account("userTA", "password", "Instructor")
        self.ui.command("login", {"username": "userTA", "password": "password"})

        # Instructor changes own email, phone number, password; expected success
        self.assertEquals(self.ui.command("edit_info", {"field": "email", "email": "erin erinfink@uwm.edu"}),
                          "Email has been updated successfully.")
        self.assertEquals(self.ui.command("edit_info", {"field": "phone", "phone": "1231231234"}),
                          "Phone Number has been updated successfully")
        self.assertEquals(self.ui.command("edit_info",
                                          {"field": "address",
                                           "address": "Address: 2311 E Hartford Ave Milwaukee, WI 53211"}),
                          "Address has been updated successfully.")

    def test_command_Administrator_change_contact_info(self):
        self.di.create_account("userTA", "password", "Administrator")
        self.ui.command("login", {"username": "userTA", "password": "password"})

        # Instructor changes own email, phone number, password; expected success
        self.assertEquals(self.ui.command("edit_info", {"field": "email", "email": "erin erinfink@uwm.edu"}),
                          "Email has been updated successfully.")
        self.assertEquals(self.ui.command("edit_info", {"field": "phone", "phone": "1231231234"}),
                          "Phone Number has been updated successfully")
        self.assertEquals(self.ui.command("edit_info",
                                          {"field": "address",
                                           "address": "Address: 2311 E Hartford Ave Milwaukee, WI 53211"}),
                          "Address has been updated successfully.")

    def test_command_edit_contact_format(self):
        self.di.create_account("userInstructor", "password", "instructor")
        self.ui.command("login", {"username": "userInstructor", "password": "password"})

        # no argument given
        self.assertEquals(self.ui.command("edit_info", {}), "ERROR")



