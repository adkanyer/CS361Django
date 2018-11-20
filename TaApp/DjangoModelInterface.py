from TaCLI.DataInterface import DataInterface
import TaCLI.User
from TaApp.models import *
import hashlib


class DjangoModelInterface(DataInterface):

    def __init__(self):
        pass

    def create_account(self, account_name, password, role):
        h = hashlib.new("md5")
        h.update(f"{password}".encode("ascii"))
        hashed_password = h.hexdigest()
        acct = Account.objects.create(name=account_name, password=hashed_password, role=role)
        ContactInfo.objects.create(account=acct, address="")

    def delete_account(self, account_name):
        Account.objects.filter(name=account_name).delete()

    def update_account(self, account_name, password, role):
        account = Account.objects.filter(name=account_name).first()
        if account is None:
            return
        h = hashlib.new("md5")
        h.update(password.encode("ASCII"))
        account.password = h.hexdigest()
        account.role = role
        account.save()

    def get_accounts(self):
        accounts = []
        account_objs = Account.objects.all()
        for acct in account_objs:
            accounts.append({"name": acct.name, "password": acct.password, "role": acct.role})
        return accounts

    def get_logged_in(self):
        logged_in = LoggedIn.objects.first()
        if logged_in is None:
            return ""
        return logged_in.account.name

    def set_logged_in(self, account_name):
        acct = Account.objects.filter(name=account_name).first()
        LoggedIn.objects.create(account=acct)

    def set_logged_out(self):
        LoggedIn.objects.all().delete()

    def create_course(self, course_number, course_name, ):
        Course.objects.create(number=course_number, name=course_name)

    def get_courses(self):
        courses = []
        for c in Course.objects.all():
            instructor = "No Instructor Assigned"
            if c.instructor.first() is not None:
                instructor = c.instructor.first().name
            tas = []
            for ta in c.tas.all():
                tas.append(ta.name)
            courses.append({"course_number": str(c.number), "course_name": c.name, "instructor": instructor, "tas": tas})
        return courses

    def set_course_assignment(self, course_number, instructor_name):
        pass

    def set_course_instructor(self, course_number, instructor_name):
        instructor = Account.objects.filter(name=instructor_name).first()
        course = Course.objects.filter(number=course_number).first()
        course.instructor.add(instructor)
        course.save()

    def add_course_ta(self, course_number, ta_name):
        ta = Account.objects.filter(name=ta_name).first()
        course = Course.objects.filter(number=course_number).first()
        course.tas.add(ta)
        course.save()

    def get_course_assignments(self):
        return []

    def create_lab(self, course_number, lab_number):
        course = Course.objects.filter(number=course_number).first()
        lab = Lab.objects.create(number=lab_number)
        course.labs.add(lab)
        course.save()

    def get_labs(self):
        labs = []
        for lab in Lab.objects.all():
            course = Course.objects.filter(labs__id=lab.id).first()
            ta_name = None
            if lab.ta is not None:
                ta_name = lab.ta.name
            labs.append({"course_number": course.number, "lab_number": lab.number, "ta_name": ta_name})
        return labs

    def set_lab_assignment(self, course_number, lab_number, ta_name):
        lab = Lab.objects.filter(number=lab_number, course__number=course_number).first()
        ta = Account.objects.filter(name=ta_name).first()
        lab.ta = ta
        lab.save()

    def get_lab_assignments(self):
        return []

    def get_user(self, user_name):
        userobj = Account.objects.filter(name=user_name).first()
        if userobj is None:
            return None
        return TaCLI.User.User(userobj.name, userobj.role, userobj.password)

    def course_exists(self, course_number):
        course = Course.objects.filter(number=course_number).first()
        return course is not None

    def is_course_assigned(self, course_number):
        course = Course.objects.filter(number=course_number).first()
        if course is not None and course.instructor.first() is not None:
            return course.instructor.first().name is not None
        return False

    def lab_exists(self, course_number, lab_number):
        lab = Lab.objects.filter(number=lab_number, course__number=course_number).first()
        return lab is not None

    def is_lab_assigned(self, course_number, lab_number):
        lab = Lab.objects.filter(number=lab_number, course__number=course_number).first()
        return lab is not None and lab.ta is not None

    def is_valid_role(self, role):
        return role in ["administrator", "supervisor", "instructor", "TA"]

    def get_private_info(self, user):
        info = ContactInfo.objects.filter(account__name=user.username).first()
        hours = OfficeHour.objects.filter(contact_info=info)
        s = ""
        s += "Username: " + user.username + "\n"
        s += "Role: " + user.role + "\n"
        if info.first_name is not None and info.last_name is not None:
            s += "Name: " + info.first_name + " " + info.last_name + "\n"
        if info.address is not None:
            s += "Address: " + info.address + "\n"
        if info.phone is not None:
            s += "Phone: " + info.phone + "\n"
        if info.email is not None:
            s += "Email: " + info.email + "\n"
        s += "Office Hours: "
        for hour in hours:
            s += hour.time + " "
        return s

    def get_public_info(self, user):
        info = ContactInfo.objects.filter(account__name=user.username).first()
        hours = OfficeHour.objects.filter(contact_info=info)
        s = ""
        s += "Username: " + user.username + "\n"
        s += "Role: " + user.role + "\n"
        if info.first_name is not None and info.last_name is not None:
            s += "Name: " + info.first_name + " " + info.last_name + "\n"
        if info.email is not None:
            s += "Email: " + info.email + "\n"
        s += "Office Hours: "
        for hour in hours:
            s += hour.time + " "
        return s

    def edit_phone(self, account_name, phone_number):
        contact = ContactInfo.objects.filter(account__name=account_name).first()
        if contact is not None:
            contact.phone = phone_number
            contact.save()

    def edit_address(self, account_name, address):
        contact = ContactInfo.objects.filter(account__name=account_name).first()
        if contact is not None:
            contact.address = address
            contact.save()

    def edit_email(self, account_name, email):
        contact = ContactInfo.objects.filter(account__name=account_name).first()
        if contact is not None:
            contact.email = email
            contact.save()

    def edit_office_hours(self, account_name, office_hours):
        contact = ContactInfo.objects.filter(account__name=account_name).first()
        print(contact)
        if contact is not None:
            OfficeHour.objects.filter(contact_info=contact).delete()
            for oh in office_hours:
                oh_obj = OfficeHour.objects.create(time=oh)
                oh_obj.contact_info.add(contact)
                oh_obj.save()


    def edit_name(self, account_name, first, last):
        contact = ContactInfo.objects.filter(account__name=account_name).first()
        if contact is not None:
                contact.first_name = first
                contact.last_name = last
                contact.save()
