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
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["supervisor"]:
            self.environment.debug("Permission Denied.")
            return "ERROR"

        if len(args) != 3:
            self.environment.debug("Invalid arguments.\nCorrect Parameters: assign_Course <COURSE NUMBER> <USERNAME>")
            return "ERROR"

        course_num = args[1]
        if not self.environment.database.course_exists(course_num):
            self.environment.debug("Course does not exist.")
            return "ERROR"

        account = self.environment.database.get_user(args[2])
        if account is None:
            self.environment.debug("Inputted user does not exist.")
            return "ERROR"

        if account.get_role() == "instructor":
            if self.environment.database.is_course_assigned(course_num):
                self.environment.debug("Course already assigned to instructor.")
                return "ERROR"
            self.environment.database.set_course_instructor(args[1], args[2])
            return "Course assigned successfully."
        elif account.get_role() == "TA":
            if self.environment.database.is_course_assigned_to_ta(course_num):
                self.environment.debug("Course already assigned to instructor.")
                return "ERROR"
            self.environment.database.add_course_ta(args[1], args[2])
            return "Course assigned successfully."
        else:
            self.environment.debug("User is not an Instructor or TA.")
            return "ERROR"


class CreateCourse(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["create_course", course_number, course_name,]
    """

    def action(self, args):

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["supervisor", "administrator"]:
            self.environment.debug("Permission Denied.")
            return "ERROR"

        if len(args) != 3:
            self.environment.debug("Invalid arguments.\nCorrect Parameters: create_course <COURSE NUMBER> <COURSE NAME>")
            return "ERROR"

        course_number = args[1]
        course_name = args[2]

        try:
            course_number = int(course_number)
        except ValueError:
            self.environment.debug("First argument should be a number.")
            return "ERROR"

        if self.environment.database.course_exists(course_number):
            self.environment.debug("Course already exists.")
            return "ERROR"

        self.environment.database.create_course(course_number, course_name)
        return "Course Created Successfully."


class ViewCourses(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        result = ""

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["instructor", "administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return "ERROR"

        list = []
        if args == "":
            courses = self.environment.database.get_courses()

            for course in courses:
                result = ""
                for ta in course['tas']:
                    result += f"{ta}, "

                list.append({"number": course['course_number'], "name": course['course_name'],
                            "instructor": course['instructor'], "tas": result})
        else:

            course = self.environment.database.get_course(args["course_number"])

            if course is not None:
                result = ""
                for temp in course.tas.all():
                    result += f"{temp.name}, "

                return {"number": course.number, "name": course.name,
                        "instructor": course.instructor.name, "tas": result}
            else:
                self.environment.debug("That course does not exist.")
                return "ERROR"

        return list

        # for course in courses:
        #     result += f"{course['course_number']} {course['course_name']}\n\tInstructor: {course['instructor']}\n\tTAs: "
        #     for ta in course['tas']:
        #         result += f"{ta}, "
        #     result += "\n"
        # return result
