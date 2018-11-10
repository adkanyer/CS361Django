from TaCLI.Components import Command


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

        if len(args) != 1:
            self.environment.debug("Invalid args.")
            return FAILURE_MESSAGE

        if self.environment.user is None:
            self.environment.debug("No user is logged in.")
            return FAILURE_MESSAGE

        self.environment.database.set_logged_out()
        self.environment.user = None
        self.environment.debug("Logged out Successful.")
        return SUCCESS_MESSAGE
