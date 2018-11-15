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
        FAILURE_MESSAGE = "Unable to edit Contact Info."

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
        if len(args) < 3:
            self.environment.debug("Unable to update Phone Number")
            return "ERROR"

        full_argument = " ".join(args[2:])

        self.environment.database.edit_phone(self.environment.user.username, full_argument)
        return "Phone Number has been updated successfully"


class EditAddress(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):

        if len(args) < 3:
            self.environment.debug("Unable to update Address.")
            return "ERROR"

        full_argument = " ".join(args[2:])

        self.environment.database.edit_address(self.environment.user.username, full_argument)
        return "Address has been updated successfully."


class EditEmail(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        if len(args) < 3:
            self.environment.debug("Unable to update Email.")
            return "ERROR"

        full_argument = "".join(args[2:])

        self.environment.database.edit_email(self.environment.user.username, full_argument)
        return "Email has been updated successfully."


class EditOfficeHours(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):

        if len(args) < 3:
            self.environment.debug("Unable to update Office Hours.")
            return "ERROR"

        hours = args[2:]
        self.environment.database.edit_office_hours(self.environment.user.username, hours)
        return "Office Hours have been updated successfully."

