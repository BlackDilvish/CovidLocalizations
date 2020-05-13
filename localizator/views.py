from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  
from .models import LocalizationsData, HealthStatus
from .forms import FileForm
from datetime import date
from datetime import datetime


import json


def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')


def home(response):
    name = response.user.username
    return render(response, "localizator/home.html", {"name":name, "upload_info":check_upload(name),
                                                      "status_info":check_status(name)}) 


def upload(response):
    name = response.user.username
    months = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
    years = [2019, 2020]

    if response.method == 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            new_file = response.FILES['uplfile']
            text = validate_json(new_file)

            if not text:
                return render(response, 'localizator/upload.html', {'form': FileForm(), "name":name,
                                                                    "error_json_message": get_error_validation(),
                                                                    "months": months, "years": years})
            if check_for_label(text):
                month = response.POST.get("choose_month") 
                year = response.POST.get("choose_year") 
                file_date = month + str(year)
                LocalizationsData.objects.filter(name=name, file_date=file_date).delete()
                data = LocalizationsData(name=name, data=text, file_date=file_date)
                data.save()

                return render(response, 'localizator/uploaded.html', {"name":name})

            else:
                return render(response, 'localizator/upload.html', {'form': FileForm(), "name":name,
                                                                    "error_json_message": get_error_format(),
                                                                    "months": months, "years": years})

    else:
        form = FileForm()

    return render(response, 'localizator/upload.html', {'form':form, "name":name,
                                                        "months": months, "years": years})


def status(response):
    name = response.user.username
    if response.method == 'POST':
        if response.POST.get("save"):
            if response.POST.get("infected_present") == "clicked":
                start_date = convert_date(response.POST.get("start_date"))
                end_date = date.today()
                status = True
                
            elif response.POST.get("infected_past") == "clicked":
                start_date = convert_date(response.POST.get("start_date"))
                end_date = convert_date(response.POST.get("end_date"))
                status = True

            else:
                start_date = date.today()
                end_date = date.today()
                status = False

            t = HealthStatus(name=name, status=status, start_date=start_date, end_date=end_date)
            if status == False:
                HealthStatus.objects.filter(name=name).delete()
                t.save()
                return render(response, "localizator/home.html", {"name":name, "upload_info":check_upload(name), "status_info":check_status(name)})

            elif status == True and check_status_dates(start_date, end_date):
                HealthStatus.objects.filter(name=name).delete()
                t.save()
                return render(response, "localizator/home.html", {"name":name, "upload_info":check_upload(name), "status_info":check_status(name)})

            else:
                return render(response, 'localizator/status.html', {"name":name, "error_date_message":get_error_date()})
    
    return render(response, 'localizator/status.html', {"name":name})


def instruction(response):
    name = response.user.username
    return render(response, "localizator/instruction.html", {"name":name})


def check_upload(name):
    if LocalizationsData.objects.filter(name=name).count() == 0:
        upload_info = "You haven't uploaded your json file yet!"
    else:
        upload_info = "You've already uploaded your localizations from "
        data = LocalizationsData.objects.filter(name=name)
        for item in data:
            upload_info += item.json_file_date() + "\n"
    return upload_info


def check_status(name):
    if HealthStatus.objects.filter(name=name).count() == 0:
         status_info = "You haven't set your health status"
    elif HealthStatus.objects.get(name=name).covid_status() == False:
        status_info = "You are healthy for now!"
    elif HealthStatus.objects.get(name=name).covid_end_date() == str(date.today()):
        status_info = "You've been infected since " + HealthStatus.objects.get(name=name).covid_start_date()
    else:
        t = HealthStatus.objects.get(name=name)
        status_info = "You were infected from " + t.covid_start_date() + " to " +  t.covid_end_date()
        
    return status_info


def convert_date(str_date):
    if str_date == "":
        return date.today()
    else:
        return datetime.strptime(str_date, '%Y-%m-%d').date()
        

def validate_json(json_string):
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


def get_error_date():
    return "Selected dates are incorrect!"


def check_for_label(text):
    return 'timelineObjects' in text


def check_status_dates(start_date, end_date):
    return start_date <= end_date and start_date <= date.today() and end_date <= date.today()
        