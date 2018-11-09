from django.db import models


# Create your models here.
class Command(models.Model):
    text = models.TextField(max_length=256)
    time = models.DateTimeField(auto_now=True)
