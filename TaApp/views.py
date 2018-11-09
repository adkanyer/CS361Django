from django.shortcuts import render
from django.views import View


# Create your views here.
from TaApp.models import Command


def doStuff(s):
    return s


class Home(View):
    def get(self,request):
        return render(request, "main/index.html")

    def post(self,request):
        current = Command()
        current.text = request.POST["command"]
        current.save()
        past = Command.objects.all()
        s = doStuff(request.POST["command"])
        return render(request, "main/index.html", {"list": s})
