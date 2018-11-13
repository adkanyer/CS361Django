import unittest
from TaCLI.User import User


class UserUnitTests(unittest.TestCase):
    def setUp(self):
        self.user = User("testUser", "TA", "pass")

    def test_user_set_username(self):
        new_name = "newUsername"
        self.user.set_username(new_name)
        self.assertEqual(self.user.username, new_name)

    def test_user_set_role(self):
        new_role = "administrator"
        self.user.set_role(new_role)
        self.assertEqual(self.user.role, new_role)

    def test_user_get_username(self):
        self.assertEqual(self.user.get_username(), "testUser")

    def test_user_get_role(self):
        self.assertEqual(self.user.get_role(), "TA")
