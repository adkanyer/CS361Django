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

        if len(args) != 3:
            self.environment.debug("Username or Password is Incorrect")
            return FAILURE_MESSAGE

        account = self.environment.database.get_user(args[1])

        if account is None:
            self.environment.debug("Username or Password is Incorrect")
            return FAILURE_MESSAGE

        h = hashlib.new("md5")
        entered_password = args[2].rstrip()
        h.update(f"{entered_password}".encode("ascii"))
        hashed_password = h.hexdigest()

        if account.password != hashed_password:
            self.environment.debug("User name or Password is Incorrect")
            return FAILURE_MESSAGE

        self.environment.database.set_logged_in(account.username)
        self.environment.user = account
        self.environment.debug("Logged in successfully")
        return SUCCESS_MESSAGE
