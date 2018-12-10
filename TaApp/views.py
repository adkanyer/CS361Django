from django.shortcuts import render
from django.views import View

from TaApp.models import Account
from TaCLI import UI, Environment
import TaCLI.User
from TaApp.DjangoModelInterface import DjangoModelInterface

import hashlib


class BaseView(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

    def init_logged_in(self, request):
        if "user" not in request.session:
            self.environ.user = None
            return
        acct = Account.objects.filter(name=request.session["user"]).first()
        if acct is not None:
            self.environ.user = self.environ.database.get_user(acct.name)
        else:
            self.environ.user = None

    def check_credentials(self, username, password):
        account = self.environ.database.get_user(username)

        if account is None or password is None:
            self.environ.debug("Username or Password is Incorrect")
            return False

        h = hashlib.new("md5")
        entered_password = password.rstrip()
        h.update(f"{entered_password}".encode("ascii"))
        hashed_password = h.hexdigest()

        if account.password != hashed_password:
            self.environ.debug("User name or Password is Incorrect")
            return False

        self.environ.user = account
        self.environ.debug("Logged in successfully")
        return True


class Home(BaseView):
    def get(self, request):
        self.init_logged_in(request)
        user = ""
        data = None
        if self.environ.user is not None:
            user = self.environ.user.username
            data = self.ui.command("view_info", "")
        return render(request, "main/index.html", {"user": user, "response": data})

    def post(self, request):
        self.init_logged_in(request)

        if request.POST["form"] == "login" and self.environ.user is None:
            if self.check_credentials(request.POST["username"], request.POST["password"]):
                request.session["user"] = request.POST["username"]
                self.environ.user = self.environ.database.get_user(request.POST["username"])

        if request.POST["form"] == "logout":
            request.session["user"] = None
            self.environ.user = None

        current_user = request.session["user"]
        data = None
        user = ""
        if current_user is not None:
            data = self.ui.command("view_info", "")
            user = self.environ.user.username
        return render(request, "main/index.html", {"user": user, "response": data,
                                                   "message": str(self.environ.message)})


class Accounts(BaseView):
    def get(self, request):
        self.init_logged_in(request)

        accounts = None
        if self.environ.user.role == "administrator" or self.environ.user.role == "supervisor":
            accounts = self.ui.command("view_accounts", "")

        return render(request, "main/account.html", {"user": self.environ.user.username, "role": self.environ.user.role,
                                                     "accounts": accounts})

    def post(self, request):
        self.init_logged_in(request)
        response = None
        user = self.environ.user.username
        role = self.environ.user.role

        accounts = None
        if role == "administrator" or role == "supervisor":
            accounts = self.ui.command("view_accounts", "")

        if request.POST["form"] == "create_account":
            response = self.ui.command("create_account", ["create_account", request.POST["new_username"],
                                                          request.POST["new_password"], request.POST["new_role"]])

        if request.POST["form"] == "view_info":
            response = self.ui.command("view_info", {"username": request.POST["username"]})

        return render(request, "main/account.html", {"user": user, "response": response,
                                                     "message": str(self.environ.message), "role": role, "accounts": accounts})


class Courses(BaseView):
    def get(self, request):
        self.init_logged_in(request)
        user = self.environ.user.username

        return render(request, "main/courses.html", {"user": user, "response": ""})

    def post(self, request):
        response = None
        self.init_logged_in(request)
        user = self.environ.user.username

        if request.POST["form"] == "create_course":
            response = self.ui.command("create_course", ["create_course", request.POST["course_number"],
                                                          request.POST["course_name"]])

        return render(request, "main/courses.html", {"user": user, "response": response, "message": str(self.environ.message)})


class Labs(BaseView):
    def get(self, request):
        self.init_logged_in(request)
        user = self.environ.user.username

        return render(request, "main/labs.html", {"user": user, "response": ""})

    def post(self, request):
        self.init_logged_in(request)
        user = self.environ.user.username
        response = None

        return render(request, "main/labs.html", {"user": user, "response": response, "message": str(self.environ.message)})


class Settings(BaseView):
    def get(self, request):
        self.init_logged_in(request)
        user = self.environ.user.username
        data = None
        if user != "":
            data = self.ui.command("view_info", "")

        return render(request, "main/settings.html", {"user": user, "old": data})

    def post(self, request):
        self.init_logged_in(request)
        user = self.environ.user.username
        data = None
        if user != "":
            data = self.ui.command("view_info", "")

        success = ""
        if request.POST["form"] == "name":
            success = self.ui.command("edit_info", {"field": "name", "first": request.POST["first_name"], "last": request.POST["last_name"]})
        if request.POST["form"] == "email":
            success = self.ui.command("edit_info", {"field": "email", "email": request.POST["email"]})
        if request.POST["form"] == "phone":
            success = self.ui.command("edit_info", {"field": "phone", "phone": request.POST["phone"]})
        if request.POST["form"] == "address":
            address = request.POST["street"] + ", " + request.POST["city"] + " " + request.POST["state"] + " " + request.POST["zip"]
            success = self.ui.command("edit_info", {"field": "address", "address": address})
        if request.POST["form"] == "office":
            time = request.POST["day_of_week"] + ": " + request.POST["start"] + "-" + request.POST["end"]
            print(time)
            success = self.ui.command("edit_info", {"field": "office_hours", "time": time})

        return render(request, "main/settings.html", {"user": user, "old": data, "message": str(self.environ.message), "success":success})

