from django.test import TestCase

from TaApp.DjangoModelInterface import DjangoModelInterface
from TaCLI.Components.AccountCommands import *
from TaCLI.Environment import Environment
from TaCLI.User import User


class CreateAccountUnitTests(TestCase):

    def setUp(self):
        di = DjangoModelInterface()
        self.environment = Environment(di, DEBUG=True)

    def test_create_account_correct_args_administrator(self):
        self.environment.user = User("root", "administrator")
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNotNone(self.environment.database.get_user(user_name))
        self.assertEqual(response, "Account created.")

    def test_create_account_correct_args_supervisor(self):
        self.environment.user = User("root", "supervisor")
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNotNone(self.environment.database.get_user(user_name))
        self.assertEqual(response, "Account created.")

    def test_create_account_correct_args_instructor(self):
        self.environment.user = User("root", "instructor")
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertEqual(response, "ERROR")

    def test_create_account_correct_args_ta(self):
        self.environment.user = User("root", "TA")
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])
        self.assertEqual(response, "ERROR")

    def test_create_account_no_permissions(self):
        self.environment.user = User("ta_acct", "TA")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNone(self.environment.database.get_user(user_name))
        self.assertEqual(response, "ERROR")

    def test_create_account_not_logged_in(self):
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNone(self.environment.database.get_user(user_name))
        self.assertEqual(response, "ERROR")

    def test_create_account_account_exists(self):
        self.environment.user = User("root", "administrator")
        user_name = "new_user"
        self.environment.database.create_account(user_name, "password", "TA")

        create_account = CreateAccount(self.environment)
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertEqual(response, "ERROR")

    def test_create_account_not_enough_args(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        response = create_account.action(["create_account"])

        self.assertEqual(response, "ERROR")

        user_name = "new_user"
        response = create_account.action(["create_account", user_name])

        self.assertEqual(response, "ERROR")
        self.assertIsNone(self.environment.database.get_user(user_name))

        response = create_account.action(["create_account", user_name, "password"])

        self.assertEqual(response, "ERROR")
        self.assertIsNone(self.environment.database.get_user(user_name))

    def test_create_account_invalid_role(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "invalid_role"])

        self.assertEqual(response, "ERROR")
        self.assertIsNone(self.environment.database.get_user(user_name))

    def test_create_account_administrator(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "pass", "administrator"])

        self.assertEqual(response, "Account created.")

    def test_create_account_supervisor(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "pass", "supervisor"])

        self.assertEqual(response, "Account created.")

    def test_create_account_instructor(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "pass", "instructor"])

        self.assertEqual(response, "Account created.")

    def test_create_account_ta(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "pass", "TA"])

        self.assertEqual(response, "Account created.")


class DeleteAccountUnitTests(TestCase):

    def setUp(self):
        di = DjangoModelInterface()
        self.environment = Environment(di, DEBUG=True)

    def test_delete_account_correct_args_administrator(self):
        self.environment.user = User("root", "administrator")
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action({"user": user_name})

        self.assertEqual(response, "Account deleted.")
        self.assertIsNone(self.environment.database.get_user(user_name))

    def test_delete_account_correct_args_supervisor(self):
        self.environment.user = User("root", "administrator")
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action({"user": user_name})

        self.assertEqual(response, "Account deleted.")
        self.assertIsNone(self.environment.database.get_user(user_name))

    def test_delete_account_that_doesnt_exist(self):
        self.environment.user = User("root", "administrator")
        user_name = "nonexisting_account"

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action({"user": user_name})

        self.assertEqual(response, "ERROR")

    def test_delete_account_no_permissions_instructor(self):
        self.environment.user = User("TA_user", "instructor")

        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action({"user": user_name})

        self.assertEqual(response, "ERROR")
        self.assertIsNotNone(self.environment.database.get_user(user_name))

    def test_delete_account_no_permissions_TA(self):
        self.environment.user = User("TA_user", "TA")

        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action({"user": user_name})

        self.assertEqual(response, "ERROR")
        self.assertIsNotNone(self.environment.database.get_user(user_name))

    def test_delete_account_not_logged_in(self):
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action({"user": user_name})

        self.assertEqual(response, "ERROR")
        self.assertIsNotNone(self.environment.database.get_user(user_name))

    def test_delete_account_no_args(self):
        self.environment.user = User("root", "administrator")
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action({"user": None})

        self.assertEqual(response, "ERROR")
        self.assertIsNotNone(self.environment.database.get_user(user_name))


class ViewAccountsUnitTests(TestCase):
    def setUp(self):
        di = DjangoModelInterface()
        self.environment = Environment(di, DEBUG=True)

    def test_view_accounts_none_in_database(self):
        self.environment.user = User("root", "administrator")
        view_command = ViewAccounts(self.environment)
        response = view_command.action({})

        self.assertEqual(response, [])

    def test_view_accounts_3_valid_in_database_administrator(self):
        self.environment.user = User("root", "administrator")
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response,  [{"role": "instructor", "username": "InstructorUser"},
                                     {"role": "administrator", "username": "AdministratorUser"},
                                     {"role": "supervisor", "username": "SupervisorUser"}])

    def test_view_accounts_3_valid_in_database_supervisor(self):
        self.environment.user = User("root", "supervisor")
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response,  [{"role": "instructor", "username": "InstructorUser"},
                                     {"role": "administrator", "username": "AdministratorUser"},
                                     {"role": "supervisor", "username": "SupervisorUser"}])

    def test_view_accounts_3_valid_in_database_instructor(self):
        self.environment.user = User("root", "instructor")
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response, "ERROR")

    def test_view_accounts_3_valid_in_database_TA(self):
        self.environment.user = User("root", "TA")
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response,  "ERROR")

    def test_view_accounts_not_logged_in(self):
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])
        self.assertEqual(response, "ERROR")

