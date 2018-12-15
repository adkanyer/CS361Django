from django.test import TestCase
from TaCLI import UI, Environment
from TaApp.DjangoModelInterface import DjangoModelInterface


class CreateCourseTests(TestCase):
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
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})

        # Command: "create_course 361 SystemsProgramming", expect success
        self.assertEqual(self.ui.command("create_course", ["create_course", "337", "SystemsProgramming"]), "Course Created Successfully.")

    def test_command_create_course_administrator(self):
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        self.assertEqual(self.ui.command("create_course", ["create_course", "337", "SystemsProgramming"]), "Course Created Successfully.")

    def test_command_create_course_instructor(self):
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        self.assertEqual(self.ui.command("create_course", ["create_course", "361", "SystemsProgramming"]),
                          "ERROR")

    def test_command_create_course_TA(self):
        self.ui.command("login", {"username": "TA", "password": "TAPassword"})
        self.assertEqual(self.ui.command("create_course", ["create_course", "361", "SystemsProgramming"]),
                         "ERROR")

    def test_command_create_course_format(self):
        # Command: "create_course", expect error, not enough arguments
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})

        self.assertEqual(self.ui.command("create_course", ["create_course"]), "ERROR")
        self.assertEqual(self.ui.command("create_course", ["create_course", "361"]), "ERROR")
        self.assertEqual(self.ui.command("create_course", ["create_course", "SystemProgramming"]), "ERROR")
        self.assertEqual(self.ui.command("create_course", ["create_course", "SystemsProgramming", "361"]), "ERROR")


    def test_command_create_course_duplicate(self):
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("create_course", ["create_course", "361", "SystemsProgramming"]), "ERROR")
