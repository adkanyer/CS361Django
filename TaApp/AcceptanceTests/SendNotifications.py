import unittest

"""
@jkuniqh
    The roles able to send out notifications are the supervisor, the administrator and the instructor

    When send_notification command is entered, it expects three arguments :
             - String (notification)
             - List (list of users)

            The response is a string, either:
             - If Successful: "Email sent"
             - If Failure: "Error sending email"
"""

class SendNotifications(unittest.TestCase):
    def setUp(self):
        self.ui = UI()

    def test_send_notifications_supervisor(self):
        self.ui.command("create_account user1 userPassword TA")
        self.ui.command("login user1 userPassword")
        # self.ui.command -> edit info to setup email
        self.ui.command("logout")

        self.ui.command("create_account userSupervisor userPassword supervisor")
        self.ui.command("login userSupervisor userPassword")
        #self.ui.command -> edit info to setup email

        notification = "Blah Blah Blah"
        self.assertEquals(self.ui.command("send_notication {notification} {user1}"), "Email sent")

    def test_send_notifications_administrator(self):
        self.ui.command("create_account user1 userPassword TA")
        self.ui.command("login user1 userPassword")
        # self.ui.command -> edit info to setup email
        self.ui.command("logout")

        self.ui.command("create_account userAdministrator userPassword administrator")
        self.ui.command("login administrator userPassword")
        #self.ui.command -> edit info to setup email

        notification = "Blah Blah Blah"
        self.assertEquals(self.ui.command("send_notication {notification} {user1}"), "Email sent")

    def test_send_notifications_instructor_to_TA(self):
        self.ui.command("create_account user1 userPassword TA")
        self.ui.command("login user1 userPassword")
        # self.ui.command -> edit info to setup email
        self.ui.command("logout")

        self.ui.command("create_account userInstructor userPassword instructor")
        self.ui.command("login userInstructor userPassword")
        #self.ui.command -> edit info to setup email

        notification = "Blah Blah Blah"
        self.assertEquals(self.ui.command("send_notication {notification} {user1}"), "Email sent")

    def test_send_notifications_instructor_to_others(self):
        self.ui.command("create_account userSupervisor userPassword supervisor")

        self.ui.command("create_account userAdministrator userPassword administrator")

        self.ui.command("create_account userInstructor userPassword instructor")
        self.ui.command("login userInstructor userPassword")
        #self.ui.command -> edit info to setup email

        notification = "Blah Blah Blah"
        self.assertEquals(self.ui.command("send_notication {notification} {userSupervisor}"),
                          "Can only send emails to TAs")
        self.assertEquals(self.ui.command("send_notication {notification} {userAdministrator}"),
                          "Can only send emails to TAs")

    def test_send_notifications_TA(self):
        self.ui.command("create_account user1 userPassword ta")
        notification = "Blah Blah Blah"

        self.ui.command("create_account userTA userPassword ta")
        self.ui.command("login userTA userPassword")

        self.assertEquals(self.ui.command("send_notication {notification} {user}"),
                          "Not supposed to send notifications through emails")

    def test_send_notifications_format(self):
        self.assertEquals(self.ui.command("send_notication {notification} {user1}"),
                          "No user is logged in to send notifications")

        self.assertEquals(self.ui.command("send_notication {notification}"), "Missing argument")
        self.assertEquals(self.ui.command("send_notication {user1}"), "Missing argument")
