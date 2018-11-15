from django.db import models


# Create your models here.
class Command(models.Model):
    text = models.TextField(max_length=256)
    time = models.DateTimeField(auto_now=True)


class OfficeHour(models.Model):
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Account(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    role = models.CharField(max_length=15)


class ContactInfo(models.Model):
    account = models.OneToOneField(Account, null=True, on_delete=models.CASCADE)
    address = models.TextField(max_length=256)
    phone = models.TextField(max_length=16)  # not sure what to set this as
    email = models.TextField(max_length=32)  # same here ^
    office_hours = models.ManyToManyField(OfficeHour)


class Lab(models.Model):
    number = models.IntegerField()
    ta = models.OneToOneField(Account, null=True,on_delete=models.CASCADE)


class Course(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    instructor = models.ManyToManyField(Account, related_name="instructor_profile")
    tas = models.ManyToManyField(Account, related_name="ta_profile")
    labs = models.ManyToManyField(Lab)


class LoggedIn(models.Model):
    account = models.OneToOneField(Account, null=True, on_delete=models.CASCADE)
