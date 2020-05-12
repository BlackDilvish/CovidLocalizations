from localizator.models import LocalizationsData
from django.shortcuts import render
from datetime import datetime, timedelta
import geopy.distance
import json


def list_meetings(request):
    name = request.user.username
    contacts = get_contacts(name)
    prepare_contacts(contacts, name)
    response_dict = dict()
    if contacts:
        response_dict = dict(list_of_meetings=contacts)
    return render(request, 'list_meetings.html', response_dict)


def get_contacts(name):
    localizations = get_localizations(name)
    contacts = list()

    for localization in localizations:
        timeline_objects = localization['data']['timelineObjects']
        for timeline_object in timeline_objects:
            if 'activitySegment' in timeline_object:
                add_activity(timeline_object, contacts)
            else:
                add_place(timeline_object, contacts)

    return contacts


def add_activity(timeline_object, contacts):
    timeline_data = timeline_object['activitySegment']
    first_place = dict(location=timeline_data['startLocation'], startTimestamp=timeline_data['duration']['startTimestampMs'],
                       endTimestamp=timeline_data['duration']['startTimestampMs'])
    second_place = dict(location=timeline_data['endLocation'], starTtimestamp=timeline_data['duration']['endTimestampMs'],
                        endTimestamp=timeline_data['duration']['endTimestampMs'])
    contacts.append(first_place)
    contacts.append(second_place)


def add_place(timeline_object, contacts):
    timeline_data = timeline_object['placeVisit']
    place = dict(location=timeline_data['location'], startTimestamp=timeline_data['duration']['startTimestampMs'],
                 endTimestamp=timeline_data['duration']['endTimestampMs'])
    contacts.append(place)


def get_localizations(name):
    return list(LocalizationsData.objects.filter(pub_date__gte=(datetime.now() - timedelta(days=38))).
                                                 exclude(name=name).values())


def prepare_contacts(contacts, name):
    user_data = list(LocalizationsData.objects.filter(pub_date__gte=(datetime.now() - timedelta(days=38))).values())
    for data in user_data:
        timeline_objects = data['data']['timelineObjects']
        for timeline_object in timeline_objects:
            for contact in contacts:
                if 'activitySegment' in timeline_object:
                    distance = get_distance_activity(contact, timeline_object)
                #else:
                    #distance = get_distance_place(contact, timeline_object)
            contact['distance'] = distance


def get_distance_place(contact, timeline_object): #conversion thanks to https://github.com/matthewrenze/google-location-scripts/blob/master/Convert.py
    first_long = int(contact['location']['longitudeE7']) / 1E7
    first_lat = int(contact['location']['latitudeE7']) / 1E7
    second_long = int(timeline_object['location']['longitudeE7']) / 1E7
    second_lat = int(timeline_object['location']['latitudeE7']) / 1E7

    point1 = (first_long, first_lat)
    point2 = (second_long, second_lat)

    distance = geopy.distance.vincenty(point1, point2)
    return distance


def get_distance_activity(contact, timeline_object):
    first_long = int(timeline_object['startLocation']['longitudeE7']) / 1E7
    first_lat = int(timeline_object['startLocation']['latitudeE7']) / 1E7
    second_long = int(timeline_object['endLocation']['longitudeE7']) / 1E7
    second_lat = int(timeline_object['endLocation']['latitudeE7']) / 1E7

    third_long = int(contact['location']['longitudeE7']) / 1E7
    third_lat = int(contact['location']['longitudeE7']) / 1E7

    point1 = (first_long, first_lat)
    point2 = (second_long, second_lat)
    point3 = (third_long, third_lat)

    distance1 = geopy.distance.vincenty(point1, point3)
    distance2 = geopy.distance.vincenty(point2, point3)

    if distance1 < distance2:
        return distance1
    else:
        return distance2
