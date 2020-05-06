from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  
from .models import LocalizationsData, HealthStatus
from .forms import FileForm, StatusForm
from datetime import date

import json

def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')

def home(response):
    name = response.user.username

    return render(response, "localizator/home.html", {"name":name, "upload_info":checkUpload(name), "status_info":checkStatus(name)}) 

def upload(response):
    name = response.user.username
    if response.method == 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            new_file = response.FILES['uplfile']
            text = validate_json(new_file)

            if not text:
                return render(response, 'localizator/upload.html', {'form': FileForm(),
                                                                    "error_json_message": get_error_validation()})
            if check_for_label(text):
                LocalizationsData.objects.filter(name=response.user.username).delete()
                data = LocalizationsData(name=response.user.username, data=text)
                data.save()
            else:
                return render(response, 'localizator/upload.html', {'form': FileForm(),
                                                                    "error_json_message": get_error_format()})

            return render(response, 'localizator/uploaded.html', {"name":name})
    else:
        form = FileForm()

    return render(response, 'localizator/upload.html', {'form':form, "name":name})

def status(response):
    name = response.user.username
    if response.method == 'POST':
        form = StatusForm(response.POST)
        if form.is_valid():
            status = form.cleaned_data["check"]
            #start_date = form.cleaned_data["start_date"]
            #end_date = form.cleaned_data["end_date"]
            t = HealthStatus(name=name, status=status, start_date=date.today(), end_date=date.today())
            HealthStatus.objects.filter(name=name).delete()
            t.save()

            return render(response, "localizator/home.html", {"name":name, "upload_info":checkUpload(name), "status_info":checkStatus(name)}) 
    else:
        form = StatusForm()
        
    return render(response, 'localizator/status.html', {"form":form, "name":name})

def checkUpload(name):
    if LocalizationsData.objects.filter(name=name).count() == 0:
        upload_info = "You haven't uploaded your json file yet!"
    else:
        upload_info = "You've already uploaded your localizations: " + LocalizationsData.objects.get(name=name).date()
    return upload_info

def checkStatus(name):
    if HealthStatus.objects.filter(name=name).count() == 0:
         status_info = "You haven't set your health status"
    elif HealthStatus.objects.get(name=name).covid_status() == False:
        status_info = "You are healthy for now!"
    else:
        status_info = "You've been infected since " + HealthStatus.objects.get(name=name).covid_start_date()
        
    return status_info


def validate_json(json_string):# thanks to: https://stackoverflow.com/questions/21334138/check-if-file-is-json-loadable
    try:
        text = json.load(json_string)
        return text

    except ValueError:
        return False

    return True


def get_error_validation():
    return "Unfortunately sent file is not valid json. Please, check your data."


def get_error_format():
    return "It seems that your file is valid JSON, but it does not contain required content"


def check_for_label(text):
    return 'timelineObjects' in text
