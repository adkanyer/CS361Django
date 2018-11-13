class Environment:
    def __init__(self, database, user=None, DEBUG=False):
        self.database = database
        self.user = user
        self.DEBUG = DEBUG

    def debug(self, message):
        if self.DEBUG:
            print(message)
