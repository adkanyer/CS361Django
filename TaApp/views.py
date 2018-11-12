from django.shortcuts import render
from django.views import View

from TaApp.models import *
from TaCLI import UI, Environment, TextFileInterface
import TaCLI.User
from TaApp.DjangoModelInterface import DjangoModelInterface


class Home(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

    def get(self, request):
        try:
            user = Account.objects.get(name=request.session['logged_in'])
            self.ui.environment.user = TaCLI.User.User(user.name, user.role)
        except (KeyError, Account.DoesNotExist):
            self.ui.environment.user = None
        user = None
        if self.ui.environment.user is not None:
            user = self.ui.environment.user.username
        return render(request, "main/index.html", {"user": user, "response":""})

    def post(self, request):
        try:
            user = Account.objects.get(name=request.session['logged_in'])
            self.environ.user = TaCLI.User.User(user.name, user.role)
        except (KeyError, Account.DoesNotExist):
            user = None

        current = Command()
        current.text = request.POST["command"]
        current.save()
        response = self.ui.command(request.POST["command"])
        user = None
        if self.ui.environment.user is not None:
            user = self.ui.environment.user.username
        request.session["logged_in"] = user
        return render(request, "main/index.html", {"user": user, "response": response})
