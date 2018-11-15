from django.contrib import admin
from TaApp.models import Command, Account, Course, Lab, LoggedIn, ContactInfo, OfficeHour

admin.site.register(Command)
admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Lab)
admin.site.register(LoggedIn)
admin.site.register(ContactInfo)
admin.site.register(OfficeHour)
