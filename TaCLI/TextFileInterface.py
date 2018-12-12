from TaCLI import DataInterface, User
import hashlib


class TextFileInterface(DataInterface.DataInterface):
    def __init__(self, account_file="account.txt",
                 login_file="login.txt",
                 course_file="course.txt",
                 course_assignment_file="course_assignment.txt",
                 lab_file="lab.txt",
                 lab_assignment_file="lab_assignment.txt",
                 relative_directory="TextDB/"):

        self.account_filename = f"{relative_directory}/{account_file}"
        self.login_filename = f"{relative_directory}/{login_file}"
        self.course_filename = f"{relative_directory}/{course_file}"
        self.course_assignment_filename = f"{relative_directory}/{course_assignment_file}"
        self.lab_filename = f"{relative_directory}/{lab_file}"
        self.lab_assignment_filename = f"{relative_directory}/{lab_assignment_file}"

    def clear_database(self):
        dbfiles = [self.account_filename,
                   self.course_filename,
                   self.course_assignment_filename,
                   self.login_filename,
                   self.lab_filename,
                   self.lab_assignment_filename
                   ]
        for file in dbfiles:
            open(file, "w").close()

    def create_account(self, account_name, password, role):
        h = hashlib.new("md5")
        h.update(f"{password}".encode("ascii"))
        hashed_password = h.hexdigest()
        account_file = open(self.account_filename, "a")
        account_file.write(f"{account_name}:{hashed_password}:{role}\n")
        account_file.close()

    def delete_account(self, account_name):
        account_file = open(self.account_filename, "r")
        lines = []
        for line in account_file:
            if line.split(":")[0] != account_name:
                lines.append(line)
        account_file.close()

        account_file = open(self.account_filename, "w")
        account_file.writelines(lines)
        account_file.close()

    def update_account(self, account_name, password, role):
        self.delete_account(account_name)
        self.create_account(account_name, password, role)

    def get_accounts(self):
        accounts = []
        account_file = open(self.account_filename, "r")
        lines = account_file.readlines()
        account_file.close()
        for line in lines:
            fields = line.split(":")
            accounts.append({"name": fields[0], "password": fields[1], "role": fields[2].rstrip()})
        return accounts

    def get_logged_in(self):
        login_file = open(self.login_filename, "r")
        logged_in_user = login_file.readline().rstrip()
        login_file.close()
        return logged_in_user

    def set_logged_in(self, account_name):
        login_file = open(self.login_filename, "w")
        login_file.write(f"{account_name}\n")
        login_file.close()

    def set_logged_out(self):
        login_file = open(self.login_filename, "w")
        login_file.close()

    def create_course(self, course_number, course_name):
        course_file = open(self.course_filename, "a")
        course_file.write(f"{course_number}:{course_name}\n")
        course_file.close()

    def get_courses(self):
        courses = []
        course_file = open(self.course_filename, "r")
        lines = course_file.readlines()
        course_file.close()
        for line in lines:
            fields = line.split(":")
            courses.append({"course_number": fields[0], "course_name": fields[1].rstrip(), "tas": [], "instructor": None})
        return courses

    def get_course(self, course_number):
        return None

    def set_course_assignment(self, course_number, instructor_name):
        course_assignment_file = open(self.course_assignment_filename, "a")
        course_assignment_file.write(f"{course_number}:{instructor_name}\n")
        course_assignment_file.close()

    def get_course_assignments(self):
        assignments = []
        course_assignment_file = open(self.course_assignment_filename, "r")
        lines = course_assignment_file.readlines()
        course_assignment_file.close()
        for line in lines:
            fields = line.split(":")
            assignments.append({"course_number": fields[0], "instructor_name": fields[1].rstrip()})
        return assignments

    def create_lab(self, course_number, lab_number):
        lab_file = open(self.lab_filename, "a")
        lab_file.write(f"{course_number}:{lab_number}\n")
        lab_file.close()

    def get_labs(self):
        labs = []
        lab_file = open(self.lab_filename, "r")
        lines = lab_file.readlines()
        lab_file.close()
        for line in lines:
            fields = line.split(":")
            labs.append({"course_number": fields[0], "lab_number": fields[1].rstrip()})
        return labs

    def set_lab_assignment(self, course_number, lab_number, ta_name):
        lab_file = open(self.lab_assignment_filename, "a")
        lab_file.write(f"{course_number}:{lab_number}:{ta_name}\n")
        lab_file.close()

    def get_lab_assignments(self):
        assignments = []
        lab_file = open(self.lab_assignment_filename, "r")
        lines = lab_file.readlines()
        lab_file.close()
        for line in lines:
            fields = line.split(":")
            if len(fields) != 3:
                break
            course_number = fields[0]
            lab_number = fields[1]
            ta_name = fields[2].rstrip()
            assignments.append({"course_number": course_number, "lab_number": lab_number, "ta_name": ta_name})
        return assignments

    def get_user(self, user_name):
        accounts = self.get_accounts()
        for account in accounts:
            if account["name"] == user_name:
                return User.User(account["name"], account["role"], account["password"])
        return None

    def course_exists(self, course_number):
        courses = self.get_courses()
        for course in courses:
            if course["course_number"] == str(course_number):
                return True
        return False

    def is_course_assigned(self, course_number):
        course_assignments = self.get_course_assignments()
        for assignment in course_assignments:
            if assignment["course_number"] == course_number:
                return True
        return False

    def lab_exists(self, course_number, lab_number):
        labs = self.get_labs()
        for lab in labs:
            if lab["course_number"] == str(course_number) and lab["lab_number"] == str(lab_number):
                return True
        return False

    def is_lab_assigned(self, course_number, lab_number):
        lab_assignments = self.get_lab_assignments()
        for assignment in lab_assignments:
            if assignment["course_number"] == course_number and assignment["lab_number"] == lab_number:
                return True
        return False

    def is_valid_role(self, role):
        roles = ["supervisor", "administrator", "instructor", "TA"]
        return role in roles
