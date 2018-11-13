import unittest
import hashlib
from TaCLI.TextFileInterface import TextFileInterface


class TextFileInterfaceUnitTests(unittest.TestCase):

    @staticmethod
    def hashed_password(password):
        h = hashlib.new("md5")
        h.update(f"{password}".encode("ascii"))
        return h.hexdigest()

    def setUp(self):
        self.tfi = TextFileInterface(
            relative_directory="TestDB/")
        self.tfi.clear_database()

    def test_constructor(self):
        self.assertIsNotNone(self.tfi.account_filename)
        self.assertIsNotNone(self.tfi.login_filename)
        self.assertIsNotNone(self.tfi.course_filename)
        self.assertIsNotNone(self.tfi.course_assignment_filename)
        self.assertIsNotNone(self.tfi.lab_filename)
        self.assertIsNotNone(self.tfi.lab_assignment_filename)

    def test_clear_database(self):
        self.tfi.create_account("account", "pass", "role")
        self.tfi.create_course("1", "course")
        self.tfi.create_lab("1", "801")
        self.tfi.set_course_assignment("1", "jayson")
        self.tfi.set_lab_assignment("1", "801", "apoorv")

        self.tfi.clear_database()

        dbfiles = [self.tfi.account_filename,
                   self.tfi.course_filename,
                   self.tfi.course_assignment_filename,
                   self.tfi.login_filename,
                   self.tfi.lab_filename,
                   self.tfi.lab_assignment_filename
                   ]
        for file in dbfiles:
            fin = open(file, "r")
            lines = fin.readlines()
            fin.close()

            self.assertEqual(lines, [])

    def test_create_account(self):
        password = "pass"
        self.tfi.create_account("account", password, "role")

        account_file = open(self.tfi.account_filename, "r")
        lines = account_file.readlines()
        account_file.close()

        self.assertEqual(lines, ["account:" + self.hashed_password(password) + ":role\n"])

    def test_delete_account(self):
        self.tfi.create_account("account", "pass", "role")
        self.tfi.create_account("account2", "pass", "role")
        self.tfi.delete_account("account")

        account_file = open(self.tfi.account_filename, "r")

        lines = []
        for line in account_file.readlines():
            lines.append(line.rstrip())

        account_file.close()

        h = hashlib.new("md5")
        h.update(b"pass")
        hashed_pass = h.hexdigest()

        self.assertEqual(lines, [f"account2:{hashed_pass}:role"])

    def test_update_account(self):
        password = "newpass"
        self.tfi.create_account("account", "pass", "role")
        self.tfi.update_account("account", password, "newrole")

        account_file = open(self.tfi.account_filename, "r")
        lines = account_file.readlines()
        account_file.close()

        self.assertEqual(lines, ["account:"+self.hashed_password(password)+":newrole\n"])

    def test_get_accounts(self):
        password1 = "pass"
        password2 = "pass2"

        self.tfi.create_account("account", password1, "role")
        self.tfi.create_account("account2", password2, "role2")

        accounts = self.tfi.get_accounts()

        self.assertEqual(accounts, [{"name":"account", "password":self.hashed_password(password1), "role":"role"},
                                    {"name":"account2","password":self.hashed_password(password2), "role":"role2"}])

    def test_get_set_logged_in(self):
        self.tfi.set_logged_in("account")

        response = self.tfi.get_logged_in()

        self.assertEqual(response, "account")

    def test_set_logged_in_set_logged_out(self):
        self.tfi.set_logged_in("account")

        response = self.tfi.get_logged_in()
        self.assertEqual(response, "account")

        self.tfi.set_logged_out()

        response = self.tfi.get_logged_in()
        self.assertEqual(response, "")

    def test_create_course_get_courses(self):
        self.tfi.create_course("361", "CompSci361")

        response = self.tfi.get_courses()

        self.assertEqual(response, [{"course_name":"CompSci361", "course_number":"361"}])

    def test_create_course_assignments_get_courses_assignments(self):
        self.tfi.set_course_assignment("361", "jayson")

        response = self.tfi.get_course_assignments()

        self.assertEqual(response, [{"instructor_name":"jayson", "course_number":"361"}])

    def test_create_lab_get_labs(self):
        self.tfi.create_lab("361", "801")

        response = self.tfi.get_labs()

        self.assertEqual(response, [{"course_number":"361", "lab_number":"801"}])

    def test_create_lab_assignment_get_lab_assignments(self):
        self.tfi.set_lab_assignment("361", "801", "apoorv")

        response = self.tfi.get_lab_assignments()

        self.assertEqual(response, [{"course_number":"361", "lab_number":"801", "ta_name":"apoorv"}])

    def test_get_user_exists(self):
        self.tfi.create_account("root", "root", "administrator")
        self.assertIsNotNone(self.tfi.get_user("root"))

    def test_get_user_doesnt_exist(self):
        self.assertIsNone(self.tfi.get_user("nonexistent"))

    # Course Test cases
    def test_get_course_exists(self):
        self.tfi.create_course("123", "test_course")
        self.assertIsNotNone(self.tfi.course_exists("123"))

    def test_get_course_doesnt_exist(self):
        self.assertIsNotNone(self.tfi.course_exists("000"))

    def test_get_course_assigned(self):
        self.tfi.create_account("teacher", "root", "instructor")
        self.tfi.create_course("123", "test_course")
        self.tfi.set_course_assignment("123", "teacher")
        self.assertTrue(self.tfi.is_course_assigned("123"))

    def test_get_course_not_assigned(self):
        self.assertFalse(self.tfi.is_course_assigned("000"))

    def test_get_lab_exists(self):
        self.tfi.create_course("123", "test_course")
        self.tfi.create_lab("123", "001")
        self.assertTrue(self.tfi.lab_exists("123", "001"))

    def test_get_lab_doesnt_exist(self):
        self.assertFalse(self.tfi.lab_exists("123", "1231231"))

    def test_get_lab_assigned(self):
        self.tfi.create_account("ta", "pass", "TA")
        self.tfi.create_course("123", "test_course")
        self.tfi.create_lab("123", "001")
        self.tfi.set_lab_assignment("123", "001", "ta")
        self.assertTrue(self.tfi.is_lab_assigned("123", "001"))

    def test_get_lab_not_assigned(self):
        self.tfi.create_course("234", "test_course2")
        self.tfi.create_lab("234", "000")
        self.assertFalse(self.tfi.is_lab_assigned("234", "000"))

    def test_valid_role_admin(self):
        self.assertTrue(self.tfi.is_valid_role("administrator"))

    def test_valid_role_supervisor(self):
        self.assertTrue(self.tfi.is_valid_role("supervisor"))

    def test_valid_role_instructor(self):
        self.assertTrue(self.tfi.is_valid_role("instructor"))

    def test_valid_role_TA(self):
        self.assertTrue(self.tfi.is_valid_role("TA"))

    def test_invalid_role(self):
        self.assertFalse(self.tfi.is_valid_role("invalid"))
