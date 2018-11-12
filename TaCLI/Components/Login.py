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

        user_list = self.environment.database.get_accounts()

        account = {}

        for i in user_list:
            if i["name"] == args[1]:
                account = i

        if len(account) == 0:
            self.environment.debug("Username or Password is Incorrect")
            return FAILURE_MESSAGE

        h = hashlib.new("md5")
        entered_password = args[2].rstrip()
        h.update(f"{entered_password}".encode("ascii"))
        hashed_password = h.hexdigest()

        print(f"acctpw: {account['password']}\npasswd: {hashed_password}")
        if account["password"] != hashed_password:
            self.environment.debug("User name or Password is Incorrect")
            return FAILURE_MESSAGE

        self.environment.database.set_logged_in(account["name"])
        self.environment.user = TaCLI.User.User(account["name"], account["role"])
        self.environment.debug("Logged in successfully")
        return SUCCESS_MESSAGE
