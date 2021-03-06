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

    def action(self, args):
        FAILURE_MESSAGE = "Unable to edit Contact Info."

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            self.environment.debug("Permission denied.")
            return "ERROR"

        if self.environment.database.get_user(args["user"]) is None:
            self.environment.debug("User to edit doesn't exist.")
            return "ERROR"

        valid_info = self.fields.keys()

        if args["field"] in valid_info:
            return self.fields[args["field"]].action(args)

        return FAILURE_MESSAGE


class EditPhone(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        user = self.environment.database.get_user(args["user"]).username
        self.environment.database.edit_phone(user, args["phone"])
        return "Phone Number has been updated successfully"


class EditAddress(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        user = self.environment.database.get_user(args["user"]).username
        self.environment.database.edit_address(user, args["address"])
        return "Address has been updated successfully."


class EditEmail(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        user = self.environment.database.get_user(args["user"]).username
        self.environment.database.edit_email(user, args["email"])
        return "Email has been updated successfully."


class EditOfficeHours(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        user = self.environment.database.get_user(args["user"]).username
        self.environment.database.edit_office_hours(user, args["time"])
        return "Office Hours have been updated successfully."


class EditName(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        user = self.environment.database.get_user(args["user"]).username
        self.environment.database.edit_name(user, args["first"], args["last"])
        return "Name has been updated successfully."
