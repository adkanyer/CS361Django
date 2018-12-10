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
        user = str(self.environ.database.get_logged_in())
        data = None
        if user != "":
            data = self.ui.command("view_info", "")

        return render(request, "main/index.html", {"user": user, "response": data})

    def post(self, request):
        if request.POST["form"] == "login":
            self.ui.command("login", {"username": request.POST["username"], "password": request.POST["password"]})
        if request.POST["form"] == "logout":
            self.ui.command("logout", "")

        user = str(self.environ.database.get_logged_in())
        data = None
        if user != "":
            data = self.ui.command("view_info", "")

        user = str(self.environ.database.get_logged_in())
        return render(request, "main/index.html", {"user": user, "response": data, "message": str(self.environ.message)})


class Accounts(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

        acct = Account.objects.filter(name=self.environ.database.get_logged_in()).first()
        if acct is not None:
            self.environ.user = TaCLI.User.User(acct.name, acct.role)

    def get(self, request):
        user = str(self.environ.database.get_logged_in())
        role = self.environ.user.role

        accounts = None
        if role == "administrator" or role == "supervisor":
            accounts = self.ui.command("view_accounts", "")

        return render(request, "main/account.html", {"user": user, "role": role, "accounts": accounts})

    def post(self, request):
        user = str(self.environ.database.get_logged_in())
        role = self.environ.user.role

        responses = {
            "create_account": "",
            "view_info": "",
            "update_info": ""
        }

        if request.POST["form"] == "create_account":
            responses["create_account"] = self.ui.command("create_account", ["create_account", request.POST["new_username"], request.POST["new_password"], request.POST["new_role"]])

        if request.POST["form"] == "view_info":
            responses["view_info"] = self.ui.command("view_info", {"username": request.POST["username"]})

        if request.POST["form"] == "name":
            responses["update_info"] = self.ui.command("update_info", {"field": "name", "user": request.POST["user"], "first": request.POST["first_name"], "last": request.POST["last_name"]})
        if request.POST["form"] == "email":
            responses["update_info"] = self.ui.command("update_info", {"field": "email", "user": request.POST["user"], "email": request.POST["email"]})
        if request.POST["form"] == "phone":
            responses["update_info"] = self.ui.command("update_info", {"field": "phone", "user": request.POST["user"], "phone": request.POST["phone"]})
        if request.POST["form"] == "address":
            address = request.POST["street"] + ", " + request.POST["city"] + " " + request.POST["state"] + " " + request.POST["zip"]
            responses["update_info"] = self.ui.command("update_info", {"field": "address", "user": request.POST["user"], "address": address})
        if request.POST["form"] == "office":
            time = request.POST["day_of_week"] + ": " + request.POST["start"] + "-" + request.POST["end"]
            responses["update_info"] = self.ui.command("update_info", {"field": "office_hours", "user": request.POST["user"], "time": time})
        if request.POST["form"] == "delete":
            responses["update_info"] = self.ui.command("delete_account", {"user": request.POST["user"]})

        accounts = None
        if role == "administrator" or role == "supervisor":
            accounts = self.ui.command("view_accounts", "")

        return render(request, "main/account.html", {"user": user, "responses": responses, "message": str(self.environ.message), "role": role, "accounts": accounts})


class Courses(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

        acct = Account.objects.filter(name=self.environ.database.get_logged_in()).first()
        if acct is not None:
            self.environ.user = TaCLI.User.User(acct.name, acct.role)

    def get(self, request):
        user = str(self.environ.database.get_logged_in())
        role = self.environ.user.role

        if role == "administrator" or role == "supervisor" or role == "instructor":
            courses = self.ui.command("view_courses", "")
        user = str(self.environ.database.get_logged_in())

        return render(request, "main/courses.html", {"user": user, "role": role, "courses": courses})

    def post(self, request):
        user = str(self.environ.database.get_logged_in())
        role = self.environ.user.role
        response = None
        courses = None

        if role == "administrator" or role == "supervisor" or role == "instructor":
            courses = self.ui.command("view_courses", "")

        if request.POST["form"] == "create_course":
            response = self.ui.command("create_course", ["create_course", request.POST["course_number"],
                                                         request.POST["course_name"]])
        response = None
        user = str(self.environ.database.get_logged_in())

        return render(request, "main/courses.html", {"user": user, "role": role, "courses": courses,
                                                     "response": response, "message": str(self.environ.message)})

class Labs(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

        acct = Account.objects.filter(name=self.environ.database.get_logged_in()).first()
        if acct is not None:
            self.environ.user = TaCLI.User.User(acct.name, acct.role)

    def get(self, request):
        user = str(self.environ.database.get_logged_in())

        return render(request, "main/labs.html", {"user": user, "response": ""})

    def post(self, request):
        response = None
        user = str(self.environ.database.get_logged_in())

        return render(request, "main/labs.html", {"user": user, "response": response, "message": str(self.environ.message)})


class Settings(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

        acct = Account.objects.filter(name=self.environ.database.get_logged_in()).first()
        if acct is not None:
            self.environ.user = TaCLI.User.User(acct.name, acct.role)

    def get(self, request):
        user = str(self.environ.database.get_logged_in())
        data = None
        if user != "":
            data = self.ui.command("view_info", "")

        return render(request, "main/settings.html", {"user": user, "old": data})

    def post(self, request):
        user = str(self.environ.database.get_logged_in())
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
            success = self.ui.command("edit_info", {"field": "office_hours", "time": time})

        return render(request, "main/settings.html", {"user": user, "old": data, "message": str(self.environ.message), "success":success})

