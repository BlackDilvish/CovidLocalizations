from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  

def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')

def home(response):
    return render(response, "localizator/home.html", {})
