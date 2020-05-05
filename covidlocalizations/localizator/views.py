from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  
from .models import LocalizationsData
from .forms import FileForm
import json

def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')

def home(response):
    name = response.user.username
    return render(response, "localizator/home.html", {"name":name}) 

def upload(response):
    if response.method == 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            newfile = response.FILES['uplfile']
            text = newfile.read()

            #Przekierowuje do nowej strony wypelnionej tekstem
            return HttpResponse(text)
    else:
        form = FileForm()

    return render(response, 'localizator/upload.html', {'form': form})