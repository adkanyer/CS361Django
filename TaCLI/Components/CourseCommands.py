from TaCLI.Components import Command


class AssignCourse(Command.Command):
    def __init__(self, environment):
        self.environment = environment
    """
        args is a list containing the following:
            ["assign_Course", course_number, account_name]
    """
    def action(self, args):
        """
        Assigns a account to a specified course
        """

        if self.environment.user is None:
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["supervisor"]:
            return "Permission Denied."

        if len(args) != 3:
            return "Invalid arguments.\nCorrect Parameters: assign_Course <COURSE NUMBER> <USERNAME>"

        course_num = args[1]
        if not self.environment.database.course_exists(course_num):
            return "Course does not exist."
        if self.environment.database.is_course_assigned(course_num):
            return "Course already assigned to instructor."

        instructor = self.environment.database.get_user(args[2])
        if instructor is None:
            return "Inputted user does not exist."

        if instructor.get_role() != "instructor":
            return "Inputted user is not an instructor."

        self.environment.database.set_course_assignment(args[1], args[2])
        return "Course assigned successfully."


class CreateCourse(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["create_course", course_number, course_name,]
    """
    def action(self, args):

        if self.environment.user is None:
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["supervisor", "administrator"]:
            return "Permission Denied."

        if len(args) != 3:
            return "Invalid arguments.\nCorrect Parameters: create_course <COURSE NUMBER> <COURSE NAME>"

        course_number = args[1]
        course_name = args[2]

        if self.environment.database.course_exists(course_number):
            return "Course already exists."

        self.environment.database.create_course(course_number, course_name)
        return "Course Created Successfully"


class ViewCourses(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        result = ""
        FAILURE_MESSAGE = "Error viewing courses."

        if len(args) != 1:
            self.environment.debug("Invalid arguments.")
            return FAILURE_MESSAGE

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return FAILURE_MESSAGE

        if self.environment.user.get_role() not in ["instructor", "administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return FAILURE_MESSAGE

        courses = self.environment.database.get_courses()
        course_assignments = self.environment.database.get_course_assignments()
        for course in courses:
            result += f"{course['course_number']} {course['course_name']}"
            for course_assignment in course_assignments:
                if course["course_number"] == course_assignment["course_number"]:
                    result += f" {course_assignment['instructor_name']}"
            result += "\n"
        return result
