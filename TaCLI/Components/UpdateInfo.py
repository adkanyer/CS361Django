from TaCLI.Components import Command


class EditInfo(Command.Command):
    def __init__(self, environment):
        self.environment = environment
        self.fields = {
            "phone": EditPhone(self.environment),
            "address": EditAddress(self.environment),
            "email": EditEmail(self.environment),
            "office_hours": EditOfficeHours(self.environment),
            "name": EditName(self.environment),
        }

    def get_usage(self):
        return ""

    def action(self, args):
        FAILURE_MESSAGE = "Unable to edit Contact Info."

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return "ERROR"

        if self.environment.database.get_user(args[1]) is None:
            self.environment.debug("User to edit doesn't exist.")
            return "ERROR"

        if len(args) < 3:
            self.environment.debug("Invalid arguments.\nCorrect Parameters: update_info <USERNAME> <FIELD> <NEW VALUE>")
            return "ERROR"

        valid_info = self.fields.keys()

        if args[2] in valid_info:
            return self.fields[args[2]].action(args)

        return FAILURE_MESSAGE


class EditPhone(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        full_argument = " ".join(args[3:])

        user = self.environment.database.get_user(args[1]).username
        self.environment.database.edit_phone(user, full_argument)
        return "Phone Number has been updated successfully"


class EditAddress(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        full_argument = " ".join(args[3:])

        user = self.environment.database.get_user(args[1]).username
        self.environment.database.edit_address(user, full_argument)
        return "Address has been updated successfully."


class EditEmail(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        full_argument = "".join(args[3:])

        user = self.environment.database.get_user(args[1]).username
        self.environment.database.edit_email(user, full_argument)
        return "Email has been updated successfully."


class EditOfficeHours(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        hours = args[3:]
        user = self.environment.database.get_user(args[1]).username
        self.environment.database.edit_office_hours(user, hours)
        return "Office Hours have been updated successfully."


class EditName(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        first_name = args[3]
        last_name = "".join(args[4:])

        user = self.environment.database.get_user(args[1]).username
        self.environment.database.edit_name(user, first_name, last_name)

        return "Name has been updated successfully."
