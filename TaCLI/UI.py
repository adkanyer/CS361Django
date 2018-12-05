from TaCLI.Components import LabCommands, CourseCommands, AccountCommands, Login, EditInfo, UpdateInfo


class UI:
    # dictionary matching strings to commands
    def __init__(self, environment):
        self.environment = environment
        self.commands = {
            "login": Login.Login(self.environment),
            "logout": Login.Logout(self.environment),
            "create_account": AccountCommands.CreateAccount(self.environment),
            "delete_account": AccountCommands.DeleteAccount(self.environment),
            "view_accounts": AccountCommands.ViewAccounts(self.environment),
            "view_info": AccountCommands.ViewInfo(self.environment),
            "create_course": CourseCommands.CreateCourse(self.environment),
            "assign_course": CourseCommands.AssignCourse(self.environment),
            "view_courses": CourseCommands.ViewCourses(self.environment),
            "create_lab": LabCommands.CreateLab(self.environment),
            "assign_lab": LabCommands.AssignLab(self.environment),
            "view_labs": LabCommands.ViewLabs(self.environment),
            "edit_info": EditInfo.EditInfo(self.environment),
            "update_info": UpdateInfo.EditInfo(self.environment)
        }

    def command(self, command, args):
        # parse input into a list, splitting by strings

        # get valid inputs that map to commands
        valid_args = self.commands.keys()

        # if command is valid initiate its action
        if args[0] in valid_args:
            return self.commands[command].action(args)
        else:
            return "Invalid Command"

    # input: command of type string
    # return: list of command separated by spaces
    @staticmethod
    def parse_commands(command):
        return command.split()
