from TaCLI.Components import Command


class CreateAccount(Command.Command):

    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["create_account", "username", "password", "role"]
    """

    def get_usage(self):
        return ""

    def action(self, args):
        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["supervisor", "administrator"]:
            self.environment.debug("Permission Denied.")
            return "ERROR"

        if len(args) != 4:
            self.environment.debug("Invalid Arguments.\nCorrect Parameters: create_account <USERNAME> <PASSWORD> <ROLE>")
            return "ERROR"

        if self.environment.database.get_user(args[1]) is not None:
            self.environment.debug("Username is already taken.")
            return "ERROR"

        if not self.environment.database.is_valid_role(args[3]):
            self.environment.debug("Invalid Role.\nValid Roles: administrator, supervisor, instructor, TA")
            return "ERROR"

        self.environment.database.create_account(args[1], args[2], args[3])

        return "Account created."


class DeleteAccount(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["delete_account", username]
    """

    def get_usage(self):
        return ""

    def action(self, args):

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return "ERROR"

        if len(args) != 2:
            self.environment.debug("Invalid arguments.\nCorrect Parameters: delete_account <USERNAME>")
            return "ERROR"

        if self.environment.database.get_user(args[1]) is None:
            self.environment.debug("User to delete doesn't exist.")
            return "ERROR"

        self.environment.database.delete_account(args[1])
        return "Account deleted."


class ViewAccounts(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        takes no arguments and returns list of all accounts in database like:
            Username Role
            Username Role
    """

    def get_usage(self):
        return ""

    def action(self, args):
        result = ""

        if len(args) != 1:
            self.environment.debug("Invalid arguments.")
            return "ERROR"

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return "ERROR"

        accounts = self.environment.database.get_accounts()
        for account in accounts:
            result += f"{account['name']} - {account['role']}\n"
        return result


class ViewInfo(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        if has no arguments, return logged in user's information:
            Username, Role, Email, Office hours, Address, Phone           

        if has one argument and argument is a valid user,

            if user is administrator or supervisor, return all information:
                Username, Role, Email, Office hours, Address, Phone

            if user is not administrator or supervisor, return public information:
                Username, Role, Email, Office hours
    """

    def get_usage(self):
        return ""

    def action(self, args):
        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if len(args) == 1:
            user = self.environment.database.get_user(self.environment.database.get_logged_in())
            return self.environment.database.get_private_info(user)
        else:
            user = self.environment.database.get_user(args[1])
            if user is not None:
                if self.environment.user.get_role() not in ["administrator", "supervisor"]:
                    return self.environment.database.get_public_info(user)
                else:
                    return self.environment.database.get_private_info(user)

            else:
                self.environment.debug("That user does not exist.")
                return "ERROR"
