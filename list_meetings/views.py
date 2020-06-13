from django.http import HttpResponse
from localizator.models import LocalizationsData, HealthStatus
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import geopy.distance
import urllib
from django import template

divider = 1E7
precision = 3


def list_meetings(request):
    name = request.user.username
    response_dict = {'name': name}
    
    if request.method == 'POST':
        month = request.POST.get("choose_month") 
        year = request.POST.get("choose_year") 
        file_date = month + str(year)
        contacts = get_contacts(name, file_date)
        if prepare_contacts(contacts, name, file_date):
            map_contacts_locations(contacts)
            clear_contacts(contacts)
            if len(contacts) > 1:
                contacts.sort(key=by_distance)
            if len(contacts) > 10:
                contacts = contacts[:10]
            if contacts:
                response_dict['list_of_meetings'] = contacts

    return render(request, 'list_meetings/list_meetings.html', response_dict)


def contact(request, lat1, lon1, lat2, lon2, inf_act, user_act, near, duration):
    username = request.user.username
    return render(request, 'list_meetings/contact.html', 
    						{'mapid': "mapid", 'lat1': lat1,
                             'lon1': lon1, 'lat2': lat2,
                             'lon2': lon2, 'name': username,
                             'inf_act': inf_act, 'user_act': user_act, 
                             'near': near, 'duration': duration})


def by_distance(contact):
    if 'distance' in contact:
        return float(contact['distance'])
    else:
        return False


def map_contacts_locations(contacts):
    for contact in contacts:
        latitude = str(round(float(contact['location']['latitudeE7'] / divider), precision))
        longitude = str(round(float(contact['location']['longitudeE7'] / divider), precision))
        contact['location'] = dict(latitude=latitude, longitude=longitude)


def clear_contacts(contacts):
    for contact in contacts:
        if 'distance' not in contact:
            contacts.remove(contact)


def get_contacts(name, file_date):
    localizations = get_localizations(name, file_date)
    contacts = list()
    for localization in localizations:
        timeline_objects = localization['data']['timelineObjects']
        status = HealthStatus.objects.get(name=localization['name'])
        for timeline_object in timeline_objects:
            if 'activitySegment' in timeline_object:
                add_activity(timeline_object, contacts, status)
            else:
                add_place(timeline_object, contacts, status)

    return contacts


def get_act_type(timeline_data):
    if "activityType" in timeline_data:
        act_type = timeline_data["activityType"]
    else:
        act_type = "unknown"
    return act_type
    

def add_activity(timeline_object, contacts, status):
    timeline_data = timeline_object['activitySegment']
    start_date_first = datetime.utcfromtimestamp(int(timeline_data['duration']['startTimestampMs'])/1000)
    start_date_second = start_date_first + timedelta(minutes=5)
    end_date_first = datetime.utcfromtimestamp(int(timeline_data['duration']['endTimestampMs'])/1000)
    end_date_second = end_date_first + timedelta(minutes=5)
    if status.start_date < end_date_first.date() and status.start_date < end_date_first.date():
        act_type = get_act_type(timeline_data)
        
        duration = int((end_date_first-start_date_first).total_seconds()/60.0) 
        first_place = dict(location=timeline_data['startLocation'], startTimestamp=start_date_first,
                       endTimestamp=end_date_first, infected_act=act_type, duration=duration)
        duration = int((end_date_second-start_date_second).total_seconds()/60.0)                
        second_place = dict(location=timeline_data['endLocation'], startTimestamp=start_date_second,
                        endTimestamp=end_date_second, infected_act=act_type, duration=duration)     
        contacts.append(first_place)
        contacts.append(second_place)


def add_place(timeline_object, contacts, status):
    timeline_data = timeline_object['placeVisit']
    start_time = datetime.utcfromtimestamp(int(timeline_data['duration']['startTimestampMs'])/1000)
    end_time = datetime.utcfromtimestamp(int(timeline_data['duration']['endTimestampMs'])/1000)

    if status.start_date < end_time.date() and status.end_date > start_time.date():
        duration = int((end_time-start_time).total_seconds()/60.0)
        place = dict(location=timeline_data['location'], startTimestamp=start_time,
                    endTimestamp=end_time, infected_act = 'NONE', duration=duration)
        contacts.append(place)


def get_localizations(name, file_date):
    localizations = list(LocalizationsData.objects.filter(file_date=file_date).exclude(name=name).values())

    for localization in localizations:
        try:
            status = HealthStatus.objects.get(name=localization['name'])
        except HealthStatus.DoesNotExist:
            localizations.remove(localization)
            continue
        if status.status is False:
            localizations.remove(localization)
        
    return localizations

def get_user_localizations(name, file_date):
    return list(LocalizationsData.objects.filter(name=name, file_date=file_date).values())
    
def prepare_contacts(contacts, name, file_date):
    user_data = get_user_localizations(name, file_date)

    if len(user_data) <= 0:
        return False
    for data in user_data:
        timeline_objects = data['data']['timelineObjects']
        for timeline_object in timeline_objects:
            convert_timeline_obj(contacts, timeline_object)
    return True


def convert_timeline_obj(contacts, timeline_object):
    for contact in contacts:
        if 'activitySegment' in timeline_object:
            if 'startLocation' not in timeline_object['activitySegment'] or \
               'endLocation' not in timeline_object['activitySegment']:
                contacts.remove(contact)
                continue
            set_distance_activity(contact, timeline_object['activitySegment'])
        else:
            if 'location' not in timeline_object['placeVisit']:
                contacts.remove(contact)
                continue
            set_distance_place(contact, timeline_object['placeVisit'])


def set_distance_place(contact, timeline_object):
    first_long = int(contact['location']['longitudeE7']) / divider
    first_lat = int(contact['location']['latitudeE7']) / divider
    second_long = int(timeline_object['location']['longitudeE7']) / divider
    second_lat = int(timeline_object['location']['latitudeE7']) / divider

    point1 = (first_long, first_lat)
    point2 = (second_long, second_lat)

    distance = geopy.distance.vincenty(point1, point2).km
    coordinates = dict(latitude=str(round(second_lat, precision)), longitude=str(round(second_long, precision)))

    if 'distance' not in contact or distance < contact['distance']:
        contact['distance'] = round(float(distance), precision)
        contact['user_loc'] = coordinates
        contact['user_act'] = 'NONE'
        if contact['distance'] < 1:
        	contact['near'] = 1
        else:
        	contact['near'] = 0


    #thanks to: https://stackoverflow.com/a/43211266, Kurt Peek for geopy distance calculation idea, licnse(as Stack Overflow answer):
    #https://creativecommons.org/licenses/by-sa/3.0/, thus this modifed code has to be available under same license
def set_distance_activity(contact, timeline_object):
    first_long = int(timeline_object['startLocation']['longitudeE7']) / divider
    first_lat = int(timeline_object['startLocation']['latitudeE7']) / divider
    second_long = int(timeline_object['endLocation']['longitudeE7']) / divider
    second_lat = int(timeline_object['endLocation']['latitudeE7']) / divider

    third_long = int(contact['location']['longitudeE7']) / divider
    third_lat = int(contact['location']['latitudeE7']) / divider

    point1 = (first_long, first_lat)
    point2 = (second_long, second_lat)
    point3 = (third_long, third_lat)
    distance1 = geopy.distance.vincenty(point1, point3).km
    distance2 = geopy.distance.vincenty(point2, point3).km

    if distance1 < distance2:
        distance = distance1
        coordinates = dict(latitude=str(round(first_lat, precision)), longitude=str(round(first_long, precision)))
    else:
        distance = distance2
        coordinates = dict(latitude=str(round(second_lat, precision)), longitude=str(round(second_long, precision)))

    act_type = get_act_type(timeline_object)

    if 'distance' not in contact or distance < contact['distance']:
        contact['distance'] = round(float(distance), precision)
        contact['user_loc'] = coordinates
        contact['user_act'] = act_type
        if contact['distance'] < 1:
        	contact['near'] = 1
        else:
        	contact['near'] = 0


