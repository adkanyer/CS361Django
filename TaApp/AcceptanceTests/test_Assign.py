from django.test import TestCase
from TaCLI import UI, Environment
from TaApp.DjangoModelInterface import DjangoModelInterface


class AssignTests(TestCase):
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

    """
        When assign_lab command is entered, it takes two arguments:
        - TA Name
        - Class Number
        The response is a string, either:
        - Success: "Assigned to lab."
        - Failure: "Error assigning to lab."
    """
    def test_assign_lab_by_supervisor_success(self):
        # Command: "assign_lab apoorv 361", expect success
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab", "361", "801", "TA"]), "Assigned to lab.")

    def test_assign_lab_by_administrator_fail(self):
        # Command: "assign_lab TA 361", expect success
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        self.assertEqual(self.ui.command("assign_course", ["assign_course", "361", "TA"]), "ERROR")

    def test_assign_lab_by_ta_fail(self):
        # Command: "assign_lab TA 361 801", expect fail
        self.ui.command("login", {"username": "TA", "password": "TAPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab", "361", "801", "TA"]), "ERROR")

    def test_assign_lab_no_class_given(self):
        # Command: "assign_lab TA", expect failure (no class given)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab", "TA"]), "ERROR")

    def test_assign_lab_no_args(self):
        # Command: "assign_lab", expect failure (no ta name given)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab"]), "ERROR")

    def test_assign_lab_not_a_ta(self):
        # Command: "assign_lab Instructor 361", expect failure (not a TA)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab", "361", "Instructor"]), "ERROR")

    """
        When assign_course command is entered, it takes two arguments:
        - Instructor Name
        - Class Number
        The response is a string, either:
        - Success: "Assigned to class."
        - Failure: "Error assigning to class."
    """
    def test_assign_course_by_supervisor(self):
        # Command: "assign_course 361 Instructor ", expect success
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})

        response = self.ui.command("assign_course", ["assign_course", "361", "Instructor"])
        self.assertEqual(response, "Course assigned successfully.")

    def test_assign_course_by_instructor(self):
        # Command: "assign_course 361 Instructor", expect failure
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        self.assertEqual(self.ui.command("assign_course", ["assign_course", "361", "Instructor"]),
                         "ERROR")

    def test_assign_course_by_ta(self):
        # Command: "assign_course 361 Instructor", expect failure
        self.ui.command("login", {"username": "TA", "password": "TAPassword"})
        self.assertEqual(self.ui.command("assign_course", ["assign_course", "361", "Instructor"]), "ERROR")

    def test_assign_course_TA(self):
        # Command: "assign_course 361 TA", expect error (not an instructor)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_course", ["assign_course", "361", "TA"]), "Course assigned successfully.")

    def test_assign_course_no_class(self):
        # Command: "assign_course Instructor", expect error (no class given)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_course", ["assign_course", "Instructor"]), "ERROR")

    def test_assign_course_no_args(self):
        # Command: "assign_course", expect error (no instructor given)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_course", ["assign_course"]), "ERROR")

    """
        When assign_lab command is entered, it takes two arguments:
        - TA Name
        - Class Number
        - Lab Number
        The response is a string, either:
        - Success: "Assigned to lab."
        - Failure: "Error assigning to Lab."
    """
    def test_assign_lab(self):
        # Command: "assign_lab 361 801 TA", expect success
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})

        response = self.ui.command("assign_lab", ["assign_lab", "361", "801", "TA"])
        self.assertEqual(response, "Assigned to lab.")

    def test_assign_lab_no_class(self):
        # Command: "assign_lab TA", expect failure (no class or lab given)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab", "TA"]), "ERROR")

    def test_assign_lab_bad_args(self):
        # Command: "assign_lab", expect failure (no ta name given)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab", "TA", "361", "801"]), "ERROR")

    def test_assign_lab_not_ta(self):
        # Command: "assign_lab 361 801 Instructor", expect failure (not a TA)
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("assign_lab", ["assign_lab", "361", "801", "Instructor"]), "ERROR")

    """
        When view_course_assignments command is entered, it takes no arguments
        The response is a string with a line for each course in format
            "{Course Number} {Course Name} {Instructor Name}"
        Fail if the logged in user does not have permission:
            "ERROR"
    """
    def test_view_instructor_assignments_by_supervisor(self):
        self.environment.database.set_course_instructor(361, "Instructor")
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEquals(self.ui.command("view_courses", "")[0]["instructor"], "Instructor")

    def test_view_instructor_assignments_by_administrator(self):
        self.environment.database.set_course_instructor(361, "Instructor")
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        self.assertEquals(self.ui.command("view_courses", "")[0]["instructor"],
                          "Instructor")

    def test_view_instructor_assignments_by_instructor(self):
        self.environment.database.set_course_instructor(361, "Instructor")
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        self.assertEquals(self.ui.command("view_courses", "")[0]["instructor"],
                          "Instructor")

    def test_view_instructor_assignments_by_ta(self):
        self.environment.database.set_course_instructor(361, "Instructor")
        self.ui.command("login", {"username": "TA", "password": "TAPassword"})
        self.assertEquals(self.ui.command("view_courses", ""),
                          "ERROR")

    """
        When view_lab_assignments command is entered, it takes no arguments
        The response is a string with a line for each course in format
            "{Course Number} {Course Name} lab {Lab Number} {TA Name}"
        Fail if logged in user does not have permissions:
            "Error viewing ta assignments."
    """
    def test_view_ta_assignments_by_supervisor(self):
        self.environment.database.set_lab_assignment(361, 801, "TA")
        self.ui.command("login", {"username": "Supervisor", "password": "SupervisorPassword"})
        self.assertEqual(self.ui.command("view_labs", ["view_labs"])[0]["ta"], "TA")

    def test_view_ta_assignments_by_administrator(self):
        self.environment.database.set_lab_assignment(361, 801, "TA")
        self.ui.command("login", {"username": "Administrator", "password": "AdministratorPassword"})
        self.assertEquals(self.ui.command("view_labs", ["view_lab_assignments"])[0]["ta"], "TA")

    def test_view_ta_assignments_by_instructor(self):
        self.environment.database.set_lab_assignment(361, 801, "TA")
        self.ui.command("login", {"username": "Instructor", "password": "InstructorPassword"})
        self.assertEquals(self.ui.command("view_labs", ["view_lab_assignments"])[0]["ta"], "TA")

    def test_view_ta_assignments_by_ta(self):
        self.environment.database.set_lab_assignment(361, 801, "TA")
        self.ui.command("login", {"username": "TA", "password": "TAPassword"})
        self.assertEquals(self.ui.command("view_labs", ["view_lab_assignments"])[0]["ta"], "TA")
