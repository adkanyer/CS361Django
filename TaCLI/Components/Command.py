import abc
import TaCLI.User


class Command(abc.ABC):
    def __init__(self, environment):
        self.environment = environment

    @abc.abstractmethod
    def action(self, args):
        pass

    def get_user(self, user_name):
        accounts = self.environment.database.get_accounts()
        for account in accounts:
            if account["name"] == user_name:
                return User.User(account["name"], account["role"])
        return None

    def course_exists(self, course_number):
        courses = self.environment.database.get_courses()
        for course in courses:
            if course["course_number"] == str(course_number):
                return True
        return False

    def course_assigned(self, course_number):
        course_assignments = self.environment.database.get_course_assignments()
        for assignment in course_assignments:
            if assignment["course_number"] == course_number:
                return True
        return False

    def lab_exists(self, course_number, lab_number):
        labs = self.environment.database.get_labs()
        for lab in labs:
            if lab["course_number"] == str(course_number) and lab["lab_number"] == str(lab_number):
                return True
        return False

    def lab_assigned(self, course_number, lab_number):
        lab_assignments = self.environment.database.get_lab_assignments()
        for assignment in lab_assignments:
            if assignment["course_number"] == course_number and assignment["lab_number"] == lab_number:
                return True
        return False

    def is_valid_role(self, role):
        roles = ["supervisor", "administrator", "instructor", "TA"]
        return role in roles
