import TaCLI.User
import hashlib
from TaCLI.Components import Command


class Login(Command.Command):

    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["login", <username>, <password>]
    """

    def action(self, args):
        SUCCESS_MESSAGE = "Logged in."
        FAILURE_MESSAGE = "Error logging in."

        if self.environment.user is not None:
            self.environment.debug("Someone else is logged in.")
            return FAILURE_MESSAGE

        if args is None or args == {}:
            self.environment.debug("No arguments in.")
            return FAILURE_MESSAGE

        if "username" not in args or "password" not in args:
            self.environment.debug("Username or Password were not given")
            return FAILURE_MESSAGE

        if args["username"] is None or args["password"] is None:
            self.environment.debug("Username or Password is Incorrect")
            return FAILURE_MESSAGE

        account = self.environment.database.get_user(args["username"])

        if account is None:
            self.environment.debug("Username or Password is Incorrect")
            return FAILURE_MESSAGE

        h = hashlib.new("md5")
        entered_password = args["password"].rstrip()
        h.update(f"{entered_password}".encode("ascii"))
        hashed_password = h.hexdigest()

        if account.password != hashed_password:
            self.environment.debug("User name or Password is Incorrect")
            return FAILURE_MESSAGE

        self.environment.database.set_logged_in(account.username)
        self.environment.user = account
        self.environment.debug("Logged in successfully")
        return SUCCESS_MESSAGE


class Logout(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
           ["logout"]
    """

    def action(self, args):
        SUCCESS_MESSAGE = "Logged out."
        FAILURE_MESSAGE = "Error logging out."

        if self.environment.user is None:
            self.environment.debug("No user is logged in.")
            return FAILURE_MESSAGE

        self.environment.database.set_logged_out()
        self.environment.user = None
        self.environment.debug("Logged out Successful.")
        return SUCCESS_MESSAGE
