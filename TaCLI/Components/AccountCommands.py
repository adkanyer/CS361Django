from TaCLI.Components import Command


class CreateAccount(Command.Command):

    def __init__(self, environment):
        self.environment = environment
    """
        args is a list containing the following:
            ["create_account", "username", "password", "role"]
    """
    def action(self, args):
        SUCCESS_MESSAGE = "Account created."
        FAILURE_MESSAGE = "Error creating account."

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return FAILURE_MESSAGE

        if self.environment.user.get_role() not in ["supervisor", "administrator"]:
            self.environment.debug("Permission Denied")
            return FAILURE_MESSAGE

        if len(args) != 4:
            self.environment.debug("Invalid Arguments")
            return FAILURE_MESSAGE

        if self.get_user(args[1]) is not None:
            self.environment.debug("Username is already taken.")
            return FAILURE_MESSAGE

        if not self.is_valid_role(args[3]):
            self.environment.debug("Invalid Role")
            return FAILURE_MESSAGE

        self.environment.database.create_account(args[1], args[2], args[3])

        return SUCCESS_MESSAGE


class DeleteAccount(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["delete_account", username]
    """
    def action(self, args):
        SUCCESS_MESSAGE = "Account deleted."
        FAILURE_MESSAGE = "Error deleting account."

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return FAILURE_MESSAGE

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            self.environment.debug("Permission denied")
            return FAILURE_MESSAGE

        if len(args) != 2:
            self.environment.debug("Invalid arguments")
            return FAILURE_MESSAGE

        if self.get_user(args[1]) is None:
            self.environment.debug("User to delete doesn't exist")
            return FAILURE_MESSAGE

        self.environment.database.delete_account(args[1])
        return SUCCESS_MESSAGE


class ViewAccounts(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        takes no arguments and returns list of all accounts in database like:
            Username Role
            Username Role
    """
    def action(self, args):
        result = ""
        FAILURE_MESSAGE = "Error viewing accounts."

        if len(args) != 1:
            self.environment.debug("Invalid arguments.")
            return FAILURE_MESSAGE

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return FAILURE_MESSAGE

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            self.environment.debug("Permission denied")
            return FAILURE_MESSAGE

        accounts = self.environment.database.get_accounts()
        for account in accounts:
            result += f"{account['name']} {account['role']}\n"
        return result
