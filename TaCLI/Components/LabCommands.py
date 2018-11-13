from TaCLI.Components import Command


class CreateLab(Command.Command):
    def __init__(self, environment):
        self.environment = environment
    """
        args is a list containing the following:
            ["create_lab", course_number, lab_number]
    """
    def action(self, args):
        SUCCESS_MESSAGE = "Lab created."
        FAILURE_MESSAGE = "Error creating lab."

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return FAILURE_MESSAGE

        if self.environment.user.get_role() not in ["instructor", "supervisor", "administrator"]:
            self.environment.debug("Permission Denied")
            return FAILURE_MESSAGE

        if len(args) != 3:
            self.environment.debug("Invalid Arguments")
            return FAILURE_MESSAGE

        course_num = args[1]
        lab_num = args[2]
        if not self.environment.database.course_exists(course_num):
            self.environment.debug("Course does not exist")
            return FAILURE_MESSAGE

        if self.environment.database.lab_exists(course_num, lab_num):
            self.environment.debug("Lab already exists")
            return FAILURE_MESSAGE

        self.environment.database.create_lab(course_num, lab_num)
        return SUCCESS_MESSAGE


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
        SUCCESS_MESSAGE = "Assigned to lab."
        FAILURE_MESSAGE = "Error assigning to lab."

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return FAILURE_MESSAGE

        if self.environment.user.get_role() not in ["instructor", "supervisor", "administrator"]:
            self.environment.debug("Permission Denied")
            return FAILURE_MESSAGE

        if len(args) != 4:
            self.environment.debug("Invalid Arguments")
            return FAILURE_MESSAGE

        course_num = args[1]
        lab_num = args[2]
        if not self.environment.database.lab_exists(course_num, lab_num):
            self.environment.debug("Lab does not exist")
            return FAILURE_MESSAGE

        if self.environment.database.is_lab_assigned(course_num, lab_num):
            self.environment.debug("Lab already assigned to a TA")
            return FAILURE_MESSAGE

        ta = self.environment.database.get_user(args[3])
        if ta is None:
            self.environment.debug("Instructor for course does not exist")
            return FAILURE_MESSAGE

        if ta.get_role() != "TA":
            self.environment.debug("Instructor for course is not an instructor")
            return FAILURE_MESSAGE

        self.environment.database.set_lab_assignment(args[1], args[2], args[3])
        self.environment.debug("Lab assigned successfully")
        return SUCCESS_MESSAGE


class ViewLabs(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        result = ""
        FAILURE_MESSAGE = "Error viewing labs."

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return FAILURE_MESSAGE

        if self.environment.user.get_role() not in ["TA", "instructor", "administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return FAILURE_MESSAGE

        if len(args) != 1:
            self.environment.debug("Invalid arguments.")
            return FAILURE_MESSAGE

        labs = self.environment.database.get_labs()
        lab_assignments = self.environment.database.get_lab_assignments()
        for lab in labs:
            result += f"{lab['course_number']} {lab['lab_number']}"
            for lab_assignment in lab_assignments:
                if lab["course_number"] == lab_assignment["course_number"] and lab["lab_number"] == lab_assignment["lab_number"]:
                    result += f" {lab_assignment['ta_name']}"
            result += "\n"
        return result
