class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def set_username(self, new_name):
        self.username = new_name

    def set_role(self, role):
        self.role = role

    def get_username(self):
        return self.username

    def get_role(self):
        return self.role
