from django.shortcuts import render
from django.views import View

from TaApp.models import Account
from TaCLI import UI, Environment
import TaCLI.User
from TaApp.DjangoModelInterface import DjangoModelInterface


class Home(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

        acct = Account.objects.filter(name=self.environ.database.get_logged_in()).first()
        if acct is not None:
            self.environ.user = TaCLI.User.User(acct.name, acct.role)

    def get(self, request):
        user = self.environ.database.get_logged_in()

        command_list = ""
        keys = self.ui.commands.keys()
        for key in keys:
            command_list += key
            command_list += "\n   Usage: " + key + " " + self.ui.commands[key].get_usage()
            command_list += "\n"

        return render(request, "main/index.html", {"user": user, "response": "", "commands": command_list})

    def post(self, request):
        response = self.ui.command(request.POST["command"])
        user = self.environ.database.get_logged_in()

        command_list = ""

        return render(request, "main/index.html", {"user": user, "response": response, "message": self.environ.message, "commands": command_list})
