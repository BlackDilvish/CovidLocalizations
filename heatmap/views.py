
from django.shortcuts import render
from list_meetings.views import get_contacts, get_user_localizations
import geopy.distance

divider = 1E7
precision = 7
minimal_distance = 0.025

def heatmap(response):
    username = response.user.username

    if response.method == 'POST':
        month = response.POST.get("choose_month") 
        year = response.POST.get("choose_year") 
        file_date = month + str(year)
        contacts = get_contacts(username, file_date)
        contacts_coordinates = get_contacts_coordinates(contacts)
        contacts_map = {}
        if len(contacts_coordinates):
            contacts_map = {'mapid': 1, 
                            'name': username, 
                            'center': [50.067, 19.910], 
                            'localizations': contacts_coordinates}
        user_localizations = get_user_localizations(username, file_date)
        user_coordinates = get_user_coordinates(user_localizations)
        user_map = {}
        if len(user_coordinates):
            user_map = {'mapid': 2, 
                        'name': username, 
                        'center': [50.067, 19.910], 
                        'localizations': user_coordinates}
        contacts_and_user_map = {}
        if len(user_coordinates) and len(contacts_coordinates):
            contacts_and_user_map = {'mapid': 3, 
                                     'name': username, 
                                     'center': [50.067, 19.910], 
                                     'localizations': get_user_and_contacts_coordinates(user_coordinates, contacts_coordinates)}

        return render(response, 'heatmap/heatmap.html', {'contacts_map': contacts_map, 
                                                         'user_map': user_map, 
                                                         'contacts_and_user_map': contacts_and_user_map, 
                                                         'name': username})
    return render(response, 'heatmap/heatmap.html', {'name': username})


def get_contacts_coordinates(contacts):
    coordinates = []

    for contact in contacts:
        latitude = round(float(contact['location']['latitudeE7'] / divider), precision)
        longitude = round(float(contact['location']['longitudeE7'] / divider), precision)
        coordinates.append([latitude, longitude])

    return coordinates


def get_user_coordinates(user_localizations):
    coordinates = []

    for data in user_localizations:
        timeline_objects = data['data']['timelineObjects']
        for timeline_object in timeline_objects:
            if 'activitySegment' in timeline_object:
                event = timeline_object['activitySegment']
                latitude = round(float(event['endLocation']['latitudeE7'] / divider), precision)
                longitude = round(float(event['endLocation']['longitudeE7'] / divider), precision)
                coordinates.append([latitude, longitude])
                latitude = round(float(event['startLocation']['latitudeE7'] / divider), precision)
                longitude = round(float(event['startLocation']['longitudeE7'] / divider), precision)
                coordinates.append([latitude, longitude])
            else:
                event = timeline_object['placeVisit']
                latitude = round(float(event['location']['latitudeE7'] / divider), precision)
                longitude = round(float(event['location']['longitudeE7'] / divider), precision)
                coordinates.append([latitude, longitude])

    return coordinates


def get_user_and_contacts_coordinates(user_coordinates, contacts_coordinates):
    final_coordinates = []
    for user_item in user_coordinates:
        for contact_item in contacts_coordinates:
                distance = geopy.distance.vincenty(user_item, contact_item).km
                if distance < minimal_distance:
                    final_coordinates.append(user_item)
                    
    return final_coordinates
