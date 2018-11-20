from TaCLI.Components import Command


class CreateLab(Command.Command):
    def __init__(self, environment):
        self.environment = environment
    """
        args is a list containing the following:
            ["create_lab", course_number, lab_number]
    """
    def action(self, args):
        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["instructor", "supervisor", "administrator"]:
            self.environment.debug("Permission Denied.")
            return "ERROR"

        if len(args) != 3:
            self.environment.debug("Invalid Arguments.\nCorrect Parameters: create_lab <COURSE NUMBER> <LAB NUMBER>")
            return "ERROR"


        course_num = args[1]
        lab_num = args[2]
        if not self.environment.database.course_exists(course_num):
            self.environment.debug("Course does not exist.")
            return "ERROR"

        if self.environment.database.lab_exists(course_num, lab_num):
            self.environment.debug("Lab already exists.")
            return "ERROR"

        self.environment.database.create_lab(course_num, lab_num)
        return "Lab created."


class AssignLab(Command.Command):

    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["assign_lab", course_number, lab_number, account_name]
    """
    def action(self, args):
        """
        Assigns a TA to a specified lab section
        """
        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["instructor"]:
            self.environment.debug("Permission Denied.")
            return "ERROR"

        if len(args) != 4:
            self.environment.debug("Invalid Arguments.\nCorrect Parameters: assign_lab <COURSE NUMBER> <LAB NUMBER> <USERNAME>")
            return "ERROR"

        course_num = args[1]
        lab_num = args[2]
        if not self.environment.database.lab_exists(course_num, lab_num):
            self.environment.debug("Lab does not exist.")
            return "ERROR"

        if self.environment.database.is_lab_assigned(course_num, lab_num):
            self.environment.debug("Lab is already assigned to a TA.")
            return "ERROR"

        ta = self.environment.database.get_user(args[3])
        if ta is None:
            self.environment.debug("Inputted user does not exist.")
            return "ERROR"

        if ta.get_role() != "TA":
            self.environment.debug("Inputted user is not a TA.")
            return "ERROR"

        self.environment.database.set_lab_assignment(args[1], args[2], args[3])
        return "Assigned to lab."


class ViewLabs(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        result = ""

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["TA", "instructor", "administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return "ERROR"

        if len(args) != 1:
            self.environment.debug("Invalid Arguments.\nCorrect Parameters: view_labs")
            return "ERROR"

        labs = self.environment.database.get_labs()
        for lab in labs:
            result += f"{lab['course_number']} {lab['lab_number']} {lab['ta_name']}"
            result += "\n"
        return result
