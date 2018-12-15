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
        FAILURE_MESSAGE = "ERROR"

        if self.environment.user is None:
            self.environment.debug("You must be logged in to perform this action.")
            return "ERROR"

        if args is None or args == {}:
            self.environment.debug("You need to specify which field of information to edit")
            return "ERROR"


        if "field" not in args or args["field"] is None:
            self.environment.debug("You need to specify the new information to edit")
            return "ERROR"

        valid_info = self.fields.keys()

        if args["field"] in valid_info:
            return self.fields[args["field"]].action(args)

        return FAILURE_MESSAGE


class EditPhone(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        self.environment.database.edit_phone(self.environment.user.username, args["phone"])
        return "Phone Number has been updated successfully"


class EditAddress(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        self.environment.database.edit_address(self.environment.user.username, args["address"])
        return "Address has been updated successfully."


class EditEmail(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        self.environment.database.edit_email(self.environment.user.username, args["email"])
        return "Email has been updated successfully."


class EditOfficeHours(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        self.environment.database.edit_office_hours(self.environment.user.username, args["time"])
        return "Office Hours have been updated successfully."


class EditName(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    def action(self, args):
        self.environment.database.edit_name(self.environment.user.username, args["first"], args["last"])
        return "Name has been updated successfully."
