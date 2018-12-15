from django.shortcuts import render
from django.views import View

from TaApp.models import Account
from TaCLI import UI, Environment
from TaApp.DjangoModelInterface import DjangoModelInterface
import hashlib


class BaseView(View):
    def __init__(self):
        self.environ = Environment.Environment(DjangoModelInterface(), DEBUG=True)
        self.ui = UI.UI(self.environ)

    def init_logged_in(self, request):
        if "user" in request.session and request.session["user"] != "":
            print("Setting logged in to " + request.session["user"])
            self.environ.user = self.environ.database.get_user(request.session["user"])
        else:
            self.environ.user = None

    def check_password(self, username, password):
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
        role = None
        data = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role
            data = self.ui.command("view_info", "")
        return render(request, "main/index.html", {"user": user, "response": data, "role": role})

    def post(self, request):
        self.init_logged_in(request)
        if request.POST["form"] == "login":
            if self.environ.user is None and self.check_password(request.POST["username"], request.POST["password"]):
                request.session["user"] = request.POST["username"]
            else:
                print("Error password doesn't match")
        if request.POST["form"] == "logout":
            request.session["user"] = ""
            self.environ.user = None

        user = ""
        role = None
        data = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role
            data = self.ui.command("view_info", "")

        return render(request, "main/index.html", {"user": user, "response": data, "message": str(self.environ.message), "role": role,})


class Accounts(BaseView):
    def get(self, request):
        self.init_logged_in(request)

        user = ""
        role = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role

        accounts = None
        if role == "administrator" or role == "supervisor":
            accounts = self.ui.command("view_accounts", "")

        return render(request, "main/account.html", {"user": user, "role": role, "accounts": accounts})

    def post(self, request):
        self.init_logged_in(request)

        user = ""
        role = None
        if self.environ.user is not None:
            user = self.environ.user.username
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


class Courses(BaseView):
    def get(self, request):
        self.init_logged_in(request)

        user = ""
        role = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role

        courses = None

        accounts = Account.objects.filter(role="TA") | Account.objects.filter(role="instructor")

        if role == "administrator" or role == "supervisor" or role == "instructor":
            courses = self.ui.command("view_courses", "")

        user = str(self.environ.database.get_logged_in())

        return render(request, "main/courses.html", {"user": user, "role": role, "courses": courses, "accounts": accounts})

    def post(self, request):
        self.init_logged_in(request)

        user = ""
        role = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role

        responses = {
            "create_course": None,
            "assign_course": None,
            "view_course": None
        }
        courses = None

        accounts = Account.objects.filter(role="TA") | Account.objects.filter(role="instructor")

        if role == "administrator" or role == "supervisor" or role == "instructor":
            courses = self.ui.command("view_courses", "")

        if request.POST["form"] == "create_course":
            responses["create_course"] = self.ui.command("create_course", ["create_course", request.POST["course_number"],
                                                                           request.POST["course_name"]])
        if request.POST["form"] == "assign_course":
            responses["assign_course"] = self.ui.command("assign_course", ["assign_course", request.POST["course_number"],
                                                                           request.POST["username"]])

        if request.POST["form"] == "view_course":
            responses["view_course"] = self.ui.command("view_courses", {"course_number": request.POST["course_number"]})

        return render(request, "main/courses.html", {"user": user, "role": role, "courses": courses,
                                                     "responses": responses, "message": str(self.environ.message), "accounts": accounts})


class Labs(BaseView):
    def get(self, request):
        self.init_logged_in(request)

        user = ""
        role = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role

        labs = None

        accounts = Account.objects.filter(role="TA")

        if role == "administrator" or role == "supervisor" or role == "instructor" or role == "TA":
            labs = self.ui.command("view_labs", ["view_labs"])

        return render(request, "main/labs.html", {"user": user, "role": role, "labs": labs, "accounts": accounts})

    def post(self, request):
        self.init_logged_in(request)

        user = ""
        role = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role

        responses = {
            "create_lab": None,
            "assign_lab": None,
        }
        labs = None

        accounts = Account.objects.filter(role="TA")

        if request.POST["form"] == "create_lab":
            responses["create_lab"] = self.ui.command("create_lab", ["create_lab", request.POST["course_number"],
                                                                     request.POST["lab_number"]])
        if request.POST["form"] == "assign_lab":
            responses["assign_lab"] = self.ui.command("assign_lab", ["assign_lab", request.POST["course_number"],
                                                                     request.POST["lab_number"], request.POST["username"]])

        if role == "administrator" or role == "supervisor" or role == "instructor" or role == "TA":
            labs = self.ui.command("view_labs", ["view_labs"])

        return render(request, "main/labs.html", {"user": user, "role": role, "labs": labs, "accounts": accounts, "responses": responses, "message": str(self.environ.message)})


class Settings(BaseView):
    def get(self, request):
        self.init_logged_in(request)

        user = ""
        role = None
        data = None
        if self.environ.user is not None:
            user = self.environ.user.username
            role = self.environ.user.role
            data = self.ui.command("view_info", "")

        return render(request, "main/settings.html", {"user": user, "role": role, "old": data})

    def post(self, request):
        self.init_logged_in(request)
        user = ""
        data = None
        if self.environ.user is not None:
            user = self.environ.user.username
            data = self.ui.command("view_info", "")
            role = self.environ.user.role

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

        return render(request, "main/settings.html", {"user": user, "role": role, "old": data, "message": str(self.environ.message), "success":success})

