from django.db import models


# Create your models here.
class Command(models.Model):
    text = models.TextField(max_length=256)
    time = models.DateTimeField(auto_now=True)


class Account(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    role = models.CharField(max_length=15)


class ContactInfo(models.Model):
    account = models.OneToOneField(Account, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, null=True)
    phone = models.CharField(max_length=16, null=True)  # not sure what to set this as
    email = models.CharField(max_length=32, null=True)  # same here ^
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)


class OfficeHour(models.Model):
    contact_info = models.ManyToManyField(ContactInfo)
    time = models.CharField(max_length=256, null=True)


class Lab(models.Model):
    number = models.IntegerField()
    ta = models.ManyToManyField(Account)


class Course(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    instructor = models.ManyToManyField(Account, related_name="instructor_profile")
    tas = models.ManyToManyField(Account, related_name="ta_profile")
    labs = models.ManyToManyField(Lab)


class LoggedIn(models.Model):
    account = models.OneToOneField(Account, null=True, on_delete=models.CASCADE)
