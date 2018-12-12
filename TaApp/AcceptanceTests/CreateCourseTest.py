import unittest
import UI, Environment
import TextFileInterface


class CreateCourseTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface.TextFileInterface(relative_directory="../UnitTests/TestDB/")
        tfi.clear_database()

        tfi.create_account("userSupervisor", "userPassword", "supervisor")
        tfi.create_account("userAdministrator", "userPassword", "administrator")
        tfi.create_account("userInstructor", "userPassword", "instructor")
        tfi.create_account("userTA", "userPassword", "TA")

        tfi.create_course("361", "CompSci361")
        tfi.create_lab("361", "801")

        environment = Environment.Environment(tfi, DEBUG=True)
        self.ui = UI.UI(environment)

    def test_command_create_course_supervisor(self):
        """
            @jkuniqh
            The only ones able to create a course are the supervisor and the administrator

            When create_course command is entered, it expects two arguments (for now, maybe later we can add more details):
             - class number
             - class name
            The response is a string, either:
             - If Successful: "Created course."
             - If Failure: "Error creating course."
        """
        # Create a supervisor account and log in as part of the setup
        self.ui.command("create_account userSupervisor userPassword supervisor")
        self.ui.command("login userSupervisor userPassword")

        # Command: "create_course 361 SystemsProgramming", expect success
        self.assertEqual(self.ui.command("create_course 337 SystemsProgramming"), "Created course.")

    def test_command_create_course_administrator(self):
        self.ui.command("login userAdministrator userPassword")
        self.assertEqual(self.ui.command("create_course 337 SystemsProgramming"), "Created course.")

    def test_command_create_course_instructor(self):
        self.ui.command("create_account userInstructor userPassword instructor")
        self.ui.command("login userInstructor userPassword")
        self.assertEqual(self.ui.command("create_course 361 SystemsProgramming"),
                          "Error creating course.")

    def test_command_create_course_TA(self):
        self.ui.command("login userInstructor userPassword")
        self.assertEqual(self.ui.command("create_course 361 SystemsProgramming"),
                          "Error creating course.")

    def test_command_create_course_format(self):
        # Command: "create_course", expect error, not enough arguments
        self.ui.command("create_account userSupervisor userPassword supervisor")
        self.ui.command("login userSupervisor userPassword")
        self.assertEqual(self.ui.command("create_course"), "Error creating course.")
        self.assertEqual(self.ui.command("create_course 361"), "Error creating course.")
        self.assertEqual(self.ui.command("create_course SystemProgramming"), "Error creating course.")
        self.assertEqual(self.ui.command("create_course SystemsProgramming 361"), "Error creating course.")


    def test_command_create_course_duplicate(self):
        self.ui.command("create_account userSupervisor userPassword supervisor")
        self.ui.command("login userSupervisor userPassword")
        self.assertEqual(self.ui.command("create_course 361 SystemsProgramming"), "Error creating course.")
