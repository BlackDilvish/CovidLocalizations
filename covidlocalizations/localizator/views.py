from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  
from .models import LocalizationsData
import json

def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')

def home(response):
    name = response.user.username
    return render(response, "localizator/home.html", {"name":name})

def test(response):
    json_data_file = '/home/jan/Python/Task2/data.json'

    with open(json_data_file, 'r') as f:
        diary = json.load(f)

    name = response.user.username

    LocalizationsData.objects.create(name=name, data=diary)

    return render(response, "localizator/home.html", {"name":name})