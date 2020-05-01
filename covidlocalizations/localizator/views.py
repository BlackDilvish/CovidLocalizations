from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  

def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')

def home(response):
    name = response.user.username
    return render(response, "localizator/home.html", {"name":name})
