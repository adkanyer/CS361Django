from TaCLI.Components import Command


class EditInfo(Command.Command):
    def __init__(self, environment):
        self.environment = environment
        self.fields = {
            "phone": EditPhone(self.environment),
            "address": EditAddress(self.environment),
            "email": EditEmail(self.environment),
            "office_hours": EditOfficeHours(self.environment)
        }

    def action(self, args):
        FAILURE_MESSAGE = "Unable to Edit Contact Info"

        if len(args) < 2:
            return FAILURE_MESSAGE

        valid_info = self.fields.keys()

        if args[1] in valid_info:
            return self.fields[args[1]].action(args)

        return FAILURE_MESSAGE


class EditPhone(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        SUCCESS_MESSAGE = "Phone Number has been updated Successfully"
        FAILURE_MESSAGE = "Unable to Update Phone Number"

        if len(args) < 3:
            return FAILURE_MESSAGE

        full_argument = " ".join(args[2:])

        self.environment.database.edit_phone(self.environment.user.username, full_argument)
        return SUCCESS_MESSAGE


class EditAddress(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        SUCCESS_MESSAGE = "Address has been updated Successfully"
        FAILURE_MESSAGE = "Unable to Update Address"

        if len(args) < 3:
            return FAILURE_MESSAGE

        full_argument = " ".join(args[2:])

        self.environment.database.edit_address(self.environment.user.username, full_argument)
        return SUCCESS_MESSAGE


class EditEmail(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        SUCCESS_MESSAGE = "Email has been updated Successfully"
        FAILURE_MESSAGE = "Unable to Update Email"

        if len(args) < 3:
            return FAILURE_MESSAGE

        full_argument = "".join(args[2:])

        self.environment.database.edit_email(self.environment.user.username, full_argument)
        return SUCCESS_MESSAGE


class EditOfficeHours(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        SUCCESS_MESSAGE = "Office Hours have been updated Successfully"
        FAILURE_MESSAGE = "Unable to Office Hours"

        if len(args) < 3:
            return FAILURE_MESSAGE

        hours = args[2:]
        print(hours)
        self.environment.database.edit_office_hours(self.environment.user.username, hours)
        return SUCCESS_MESSAGE
