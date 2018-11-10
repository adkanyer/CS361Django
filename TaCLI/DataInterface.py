import abc

class DataInterface(abc.ABC):

    @abc.abstractmethod
    def create_account(self, account_name, password, role):
        pass

    @abc.abstractmethod
    def delete_account(self, account_name):
        pass

    @abc.abstractmethod
    def update_account(self, account_name, password, role):
        pass

    @abc.abstractmethod
    def get_accounts(self):
        pass

    @abc.abstractmethod
    def get_logged_in(self):
        pass

    @abc.abstractmethod
    def set_logged_in(self, account_name):
        pass

    @abc.abstractmethod
    def set_logged_out(self):
        pass

    @abc.abstractmethod
    def create_course(self, course_number, course_name, ):
        pass

    @abc.abstractmethod
    def get_courses(self):
        pass

    @abc.abstractmethod
    def set_course_assignment(self, course_number, instructor_name):
        pass

    @abc.abstractmethod
    def get_course_assignments(self):
        pass

    @abc.abstractmethod
    def create_lab(self, course_number, lab_number):
        pass

    @abc.abstractmethod
    def get_labs(self):
        pass

    @abc.abstractmethod
    def set_lab_assignment(self, course_number, lab_number, ta_name):
        pass

    @abc.abstractmethod
    def get_lab_assignments(self):
        pass
