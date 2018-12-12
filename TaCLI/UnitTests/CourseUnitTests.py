import unittest
from TaCLI.TextFileInterface import TextFileInterface
from TaCLI.Components.CourseCommands import CreateCourse, AssignCourse, ViewCourses
from TaCLI.Environment import Environment
from TaCLI.User import User


class CreateCourseUnitTests(unittest.TestCase):

    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()

    def test_create_course_correct_args(self):
        self.environment.user = User("root", "supervisor")
        create_course = CreateCourse(self.environment)
        response = create_course.action(["create_course", "1", "course1"])

        self.assertTrue(self.environment.database.course_exists("1"))
        self.assertEqual(response, "Course Created Successfully.")

        self.environment.user = User("subroot", "administrator")
        create_course = CreateCourse(self.environment)
        response = create_course.action(["create_course", "2", "course2"])

        self.assertTrue(self.environment.database.course_exists("2"))
        self.assertEqual(response, "Course Created Successfully.")

    def test_create_course_no_permissions(self):
        self.environment.user = User("instructor_acct", "instructor")

        create_course = CreateCourse(self.environment)
        response = create_course.action(["create_course", "1", "course1"])

        self.assertFalse(self.environment.database.course_exists("1"))
        self.assertEqual(response, "ERROR")

        self.environment.user = User("ta_acct", "TA")

        create_course = CreateCourse(self.environment)
        response = create_course.action(["create_course", "2", "course2"])

        self.assertFalse(self.environment.database.course_exists("2"))
        self.assertEqual(response, "ERROR")

    def test_create_course_not_logged_in(self):
        create_course = CreateCourse(self.environment)
        response = create_course.action(["create_course", "1", "course1"])

        self.assertFalse(self.environment.database.course_exists("1"))
        self.assertEqual(response, "ERROR")

    def test_create_course_course_exists(self):
        self.environment.user = User("root", "supervisor")
        self.environment.database.create_course("1", "course1")

        create_course = CreateCourse(self.environment)
        response = create_course.action(["create_course", "1", "course1"])

        self.assertEqual(response, "ERROR")

    def test_create_account_not_enough_args(self):
        self.environment.user = User("root", "supervisor")

        create_course = CreateCourse(self.environment)
        response = create_course.action(["create_course"])

        self.assertEqual(response, "ERROR")

        course_id = "1"

        response = create_course.action(["create_course", course_id])

        self.assertEqual(response, "ERROR")
        self.assertFalse(self.environment.database.course_exists(course_id))


class AssignCourseUnitTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "supervisor")
        self.environment.database.create_course("361", "SoftwareEngineering")

    def test_assign_course_correct_args_and_permissions(self):
        self.environment.user = User("root", "supervisor")
        self.environment.database.create_account("jayson", "password", "instructor")

        course_number = "361"
        assign_command = AssignCourse(self.environment)
        response = assign_command.action(["assign_course", course_number, "jayson"])

        self.assertTrue(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "Course assigned successfully.")

        self.environment.user = User("root", "supervisor")

    def test_assign_course_no_permissions(self):
        self.environment.user = User("admin", "administrator")

        course_number = "361"
        assign_command = AssignCourse(self.environment)
        response = assign_command.action(["assign_course", course_number, "jayson"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

        self.environment.user = User("jayson", "instructor")
        response = assign_command.action(["assign_course", course_number, "jayson"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

        self.environment.user = User("apoorv", "TA")
        response = assign_command.action(["assign_course", course_number, "jayson"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

    def test_assign_course_not_logged_in(self):
        course_number = "361"
        assign_command = AssignCourse(self.environment)
        response = assign_command.action(["assign_course", course_number, "jayson"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

    def test_assign_course_wrong_num_args(self):
        self.environment.user = User("root", "supervisor")

        course_number = "361"
        assign_command = AssignCourse(self.environment)
        response = assign_command.action(["assign_course", course_number])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

    def test_assign_course_that_doesnt_exist(self):
        self.environment.user = User("root", "supervisor")

        course_number = "1000000"
        assign_command = AssignCourse(self.environment)
        response = assign_command.action(["assign_course", course_number, "jayson"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

    def test_assign_course_that_already_assigned(self):
        self.environment.user = User("root", "supervisor")

        course_number = "361"

        assign_command = AssignCourse(self.environment)
        self.environment.database.set_course_assignment(course_number, "jayson")
        self.assertTrue(self.environment.database.is_course_assigned(course_number))

        response = assign_command.action(["assign_course", course_number, "newUser"])

        self.assertEqual(response, "ERROR")

    def test_assign_course_to_nonexistant_user(self):
        self.environment.user = User("root", "supervisor")

        course_number = "361"
        assign_command = AssignCourse(self.environment)
        response = assign_command.action(["assign_course", course_number, "IDontExist"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

    def test_assign_course_to_not_an_instructor(self):
        self.environment.user = User("root", "supervisor")
        self.environment.database.create_account("admin", "password", "administrator")
        self.environment.database.create_account("supervisor", "password", "supervisor")
        self.environment.database.create_account("ta", "password", "TA")

        course_number = "361"
        assign_command = AssignCourse(self.environment)
        response = assign_command.action(["assign_course", course_number, "admin"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

        response = assign_command.action(["assign_course", course_number, "supervisor"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")

        response = assign_command.action(["assign_course", course_number, "TA"])

        self.assertFalse(self.environment.database.is_course_assigned(course_number))
        self.assertEqual(response, "ERROR")


class ViewCoursesUnitTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "supervisor")

        self.environment.database.create_course("361", "SoftwareEngineering")

        self.environment.database.create_account("jayson", "password", "instructor")

        self.environment.database.set_course_assignment("361", "jayson")

    def test_view_courses_not_logged_in(self):
        view_command = ViewCourses(self.environment)
        response = view_command.action(["view_courses"])

        self.assertEqual(response, "ERROR")

    def test_view_courses_wrong_num_args(self):
        self.environment.user = User("root", "supervisor")
        view_command = ViewCourses(self.environment)
        response = view_command.action({"course_number": None, "extraarg": "extraBogusArg"})

        self.assertEqual(response, "ERROR")

    # really dumb test - any role can view labs
    def test_view_courses_no_permissions(self):
        self.environment.user = User("bogusUser", "bogusRole")
        view_command = ViewCourses(self.environment)
        response = view_command.action({})

        self.assertEqual(response, "ERROR")

        self.environment.user = User("apoorv", "TA")
        view_command = ViewCourses(self.environment)
        response = view_command.action({})

        self.assertEqual(response, "ERROR")

    def test_view_courses_correct(self):
        self.environment.user = User("root", "supervisor")
        view_command = ViewCourses(self.environment)
        response = view_command.action('')

        self.assertEqual(response,  [{'number': '361', 'name': 'SoftwareEngineering', 'instructor': None,  'tas':''}])
