from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(
        request=request,
        template_name="index.html"
    )

def login(request):
    return render(
        request=request,
        template_name="login.html"
    )

def config(request):
    return render(
        request=request,
        template_name="config.html"
    )

