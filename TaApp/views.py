from django.shortcuts import render
from django.views import View


# Create your views here.
from TaApp.models import *
from TaCLI import UI, Environment, TextFileInterface
import TaCLI.User

def doStuff(s):
    return s


class Home(View):
    def __init__(self):
        self.environ = Environment.Environment(TextFileInterface.TextFileInterface())
        self.ui = UI.UI(self.environ)

    def get(self, request):
        try:
            user = User.objects.get(name=request.session['user'])
            self.environ.user = TaCLI.User.User(user.name, user.role)
        except (KeyError, User.DoesNotExist):
            user = None
        return render(request, "main/index.html", {"user": self.ui.environment.user, "response":""})

    def post(self, request):
        try:
            user = User.objects.get(name=request.session['user'])
            self.environ.user = TaCLI.User.User(user.name, user.role)
        except (KeyError, User.DoesNotExist):
            user = None

        current = Command()
        current.text = request.POST["command"]
        current.save()
        response = self.ui.command(request.POST["command"])
        if self.ui.environment.user is not None:
            username = self.ui.environment.user.username
        else:
            username = ""
        request.session["user"] = username
        return render(request, "main/index.html", {"user": username, "response": response})
