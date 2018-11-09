from django.db import models


# Create your models here.
class Command(models.Model):
    text = models.TextField(max_length=256)
    time = models.DateTimeField(auto_now=True)


class OfficeHour(models.Model):
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()


class ContactInfo(models.Model):
    address = models.TextField(max_length=256)
    office_hours = models.ManyToManyField(OfficeHour)


class User(models.Model):
    name = models.TextField(max_length=30)
    email = models.EmailField()
    role = models.TextField(max_length=30)
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE)


class Lab(models.Model):
    number = models.IntegerField()
    ta = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    number = models.IntegerField()
    name = models.TextField(max_length=30)
    instructor = models.ManyToManyField(User, related_name="instructor_profile")
    tas = models.ManyToManyField(User, related_name="ta_profile")
    labs = models.ManyToManyField(Lab)

