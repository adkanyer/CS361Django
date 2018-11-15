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
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["instructor", "supervisor", "administrator"]:
            return "Permission Denied."

        if len(args) != 3:
            return "Invalid Arguments.\nCorrect Parameters: create_lab <COURSE NUMBER> <LAB NUMBER>"

        course_num = args[1]
        lab_num = args[2]
        if not self.environment.database.course_exists(course_num):
            return "Course does not exist."

        if self.environment.database.lab_exists(course_num, lab_num):
            return "Lab already exists."

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
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["instructor", "supervisor", "administrator"]:
            return "Permission Denied."

        if len(args) != 4:
            return "Invalid Arguments.\nCorrect Parameters: assign_lab <COURSE NUMBER> <LAB NUMBER> <USERNAME>"

        course_num = args[1]
        lab_num = args[2]
        if not self.environment.database.lab_exists(course_num, lab_num):
            return "Lab does not exist."

        if self.environment.database.is_lab_assigned(course_num, lab_num):
            return "Lab is already assigned to a TA."

        ta = self.environment.database.get_user(args[3])
        if ta is None:
            return "Inputted user does not exist."

        if ta.get_role() != "TA":
            return "Inputted user is not a TA."

        self.environment.database.set_lab_assignment(args[1], args[2], args[3])
        return "Assigned to lab."


class ViewLabs(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        result = ""

        if self.environment.user is None:
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["TA", "instructor", "administrator", "supervisor"]:
            return "Permission denied."

        if len(args) != 1:
            return "Invalid Arguments.\nCorrect Parameters: view_labs"

        labs = self.environment.database.get_labs()
        lab_assignments = self.environment.database.get_lab_assignments()
        for lab in labs:
            result += f"{lab['course_number']} {lab['lab_number']}"
            for lab_assignment in lab_assignments:
                if lab["course_number"] == lab_assignment["course_number"] and lab["lab_number"] == lab_assignment["lab_number"]:
                    result += f" {lab_assignment['ta_name']}"
            result += "\n"
        return result
