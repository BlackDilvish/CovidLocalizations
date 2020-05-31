from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from .models import LocalizationsData, HealthStatus
from .forms import FileForm
from datetime import date
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
import json
import list_meetings.views as list_meetings

#thanks to: https://startcodingnow.com/making-your-own-email-templates-in-django/, for way of sending html template in e-mail


def index(response):
    return HttpResponse('Strona covid local <a href="/home">home</a>')


def home(response):
    name = response.user.username
    return render(response, "localizator/home.html", {"name":name, "upload_info":check_upload(name),
                                                      "status_info":check_status(name)}) 


def upload(response):
    name = response.user.username

    if response.method == 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            new_file = response.FILES['uplfile']
            text = validate_json(new_file)
            if not text:
                return render(response, 'localizator/upload.html', {'form': FileForm(), "name":name,
                                                                    "error_json_message": get_error_validation()})
            if check_for_label(text):
                month = response.POST.get("choose_month") 
                year = response.POST.get("choose_year") 
                file_date = month + str(year)
                user = User.objects.get(username=name)
                LocalizationsData.objects.filter(name=name, file_date=file_date).delete()
                data = LocalizationsData(name=name, data=text, file_date=file_date)
                data.save()
                print(user.email)
                check_if_met_sick_person(text, file_date, name, user.email)
                return render(response, 'localizator/uploaded.html', {"name":name})
            else:
                return render(response, 'localizator/upload.html', {'form': FileForm(), "name":name,
                                                                    "error_json_message": get_error_format()})
    else:
        form = FileForm()

    return render(response, 'localizator/upload.html', {'form':form, "name":name})


def check_if_met_sick_person(json_data, file_date, name, email):
    contacts = list_meetings.get_contacts(name, file_date)
    prepare_contacts(contacts, json_data)
    contacts.sort(key=list_meetings.by_distance)
    contacts = contacts[:10]
    if len(contacts):
        execute_mail(contacts, email)


def prepare_contacts(contacts, json_data):
    timeline_objects = json_data['timelineObjects']
    for timeline_object in timeline_objects:
        list_meetings.convert_timeline_obj(contacts, timeline_object)

    for contact in contacts:
        if 'distance' not in contact or contact['distance'] >= 0.25:
            contacts.remove(contact)


def execute_mail(contacts, email):
    list_meetings.map_contacts_locations(contacts)
    add_url_to_contacts(contacts)
    message = render_to_string('list_meetings/list_meeting_table.html', dict(list_of_meetings=contacts)).strip();
    title = get_mail_title()
    no_html_str = get_no_html()
    mail_address = get_mail_address()

    send_mail(
        subject=title,
        message=no_html_str,
        html_message=message,
        from_email=mail_address,
        recipient_list=[email],
        fail_silently=False,
    )


def add_url_to_contacts(contacts):
    start_str = "https://covidlocalizations.herokuapp.com/list-meetings/contact"
    for contact in contacts:
        contact['url'] = start_str + '/' + contact['location']['latitude'] + '/' + contact['location']['longitude'] \
                         + '/' + contact['user_loc']['latitude'] + '/' + contact['user_loc']['longitude'] + '/' + \
                         contact['infected_act'] + '/' + contact['user_act'] + '/' + str(contact['near']) + '/' + \
                         str(contact['duration'])


def get_mail_address():
    return 'covid-localizations@no-reply.com'


def get_mail_title():
    return '[COVID LOCALIZATIONS] Important! Possible contact with infected person occured.',


def get_no_html():
    return 'There is a chance that you had close contacts (smaller than 250m) in following places: \n'


def status(response):
    name = response.user.username

    if response.method == 'POST' and response.POST.get("save"):
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
    upload_info = []
    if LocalizationsData.objects.filter(name=name).count() == 0:
        upload_info.append("You haven't uploaded your json file yet!")
    else:
        upload_info.append("You've already uploaded your localizations from:")
        data = LocalizationsData.objects.filter(name=name)
        for item in data:
            upload_info.append(item.json_file_date())

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
        status_info = "You were infected from " + t.covid_start_date() + " to " +  t.covid_end_date() + "."

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
