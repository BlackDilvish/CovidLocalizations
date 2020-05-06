from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  
from .models import LocalizationsData
from .forms import FileForm
import json

def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')

def home(response):
    name = response.user.username
    if LocalizationsData.objects.filter(name=name).count() == 0:
        upload_info = "You haven't uploaded your json file yet!"
    else:
        upload_info = "You've already uploaded your localizations: "

    return render(response, "localizator/home.html", {"name":name, "upload_info":upload_info}) 

def upload(response):
    name = response.user.username
    if response.method == 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            newfile = response.FILES['uplfile']
            text = json.load(newfile)
            LocalizationsData.objects.filter(name=response.user.username).delete()
            data = LocalizationsData(name=response.user.username, data=text)
            data.save()
            return render(response, 'localizator/uploaded.html', {"name":name})
    else:
        form = FileForm()

    return render(response, 'localizator/upload.html', {'form': form, "name":name})
