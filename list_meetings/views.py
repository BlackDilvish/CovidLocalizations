from localizator.models import LocalizationsData, HealthStatus
from django.shortcuts import render
from datetime import datetime, timedelta
import geopy.distance
import json


def list_meetings(request):
    name = request.user.username
    contacts = get_contacts(name)
    prepare_contacts(contacts, name)
    contacts.sort(key=by_distance)
    if len(contacts) > 10:
        contacts = contacts[:10]
    response_dict = dict()
    if contacts:
        response_dict = dict(list_of_meetings=contacts)
    return render(request, 'list_meetings.html', response_dict)


def by_distance(contact):
    return float(contact['distance'])


def get_contacts(name):
    localizations = get_localizations(name)
    contacts = list()

    for localization in localizations:
        timeline_objects = localization['data']['timelineObjects']
        #start_compare = localization['sra']
        #end_compare = localization['']

        for timeline_object in timeline_objects:
            if 'activitySegment' in timeline_object:
                add_activity(timeline_object, contacts)
            else:
                add_place(timeline_object, contacts)

    return contacts


def add_activity(timeline_object, contacts):
    timeline_data = timeline_object['activitySegment']
    start_date_first = timeline_data['duration']['startTimestampMs']
    start_date_second = timeline_data['duration']['endTimestampMs']
    end_date_first = start_date_first
    end_date_second = start_date_second

    first_place = dict(location=timeline_data['startLocation'], startTimestamp=start_date_first,
                       endTimestamp=end_date_first)
    second_place = dict(location=timeline_data['endLocation'], startTimestamp=start_date_second,
                        endTimestamp=end_date_second)
    contacts.append(first_place)
    contacts.append(second_place)


def add_place(timeline_object, contacts):
    timeline_data = timeline_object['placeVisit']
    place = dict(location=timeline_data['location'], startTimestamp=timeline_data['duration']['startTimestampMs'],
                 endTimestamp=timeline_data['duration']['endTimestampMs'])
    contacts.append(place)


def get_localizations(name):
    localizations = list(LocalizationsData.objects.filter(pub_date__gte=(datetime.now() - timedelta(days=38))).
                                                 exclude(name=name).values())
    for localization in localizations:#thanks to: https://stackoverflow.com/questions/5508888/matching-query-does-not-exist-error-in-django
        try:
            status = HealthStatus.objects.get(name=localization['name'])
        except HealthStatus.DoesNotExist:
            localizations.remove(localization)
            continue

        if status.status is False:
            localizations.remove(localization)

    return localizations


def prepare_contacts(contacts, name):
    user_data = list(LocalizationsData.objects.filter(name=name).filter(pub_date__gte=(datetime.now() - timedelta(days=38))).values())
    for data in user_data:
        timeline_objects = data['data']['timelineObjects']
        for timeline_object in timeline_objects:
            for contact in contacts:
                if 'activitySegment' in timeline_object:
                    if 'startLocation' not in timeline_object['activitySegment'] or 'endLocation' \
                            not in timeline_object['activitySegment']:
                        contacts.remove(contact)
                        continue
                    distance = get_distance_activity(contact, timeline_object['activitySegment'])
                else:
                    if 'location' not in timeline_object['placeVisit']:
                        contacts.remove(contact)
                        continue
                    distance = get_distance_place(contact, timeline_object['placeVisit'])

                contact['distance'] = distance


#calculations thanks to: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def get_distance_place(contact, timeline_object): #conversion thanks to https://github.com/matthewrenze/google-location-scripts/blob/master/Convert.py
    first_long = int(contact['location']['longitudeE7']) / 1E7
    first_lat = int(contact['location']['latitudeE7']) / 1E7
    second_long = int(timeline_object['location']['longitudeE7']) / 1E7
    second_lat = int(timeline_object['location']['latitudeE7']) / 1E7

    point1 = (first_long, first_lat)
    point2 = (second_long, second_lat)

    distance = geopy.distance.vincenty(point1, point2).km
    return distance


def get_distance_activity(contact, timeline_object):
    first_long = int(timeline_object['startLocation']['longitudeE7']) / 1E7
    first_lat = int(timeline_object['startLocation']['latitudeE7']) / 1E7
    second_long = int(timeline_object['endLocation']['longitudeE7']) / 1E7
    second_lat = int(timeline_object['endLocation']['latitudeE7']) / 1E7

    third_long = int(contact['location']['longitudeE7']) / 1E7
    third_lat = int(contact['location']['latitudeE7']) / 1E7

    point1 = (first_long, first_lat)
    point2 = (second_long, second_lat)
    point3 = (third_long, third_lat)

    distance1 = geopy.distance.vincenty(point1, point3).km
    distance2 = geopy.distance.vincenty(point2, point3).km

    if distance1 < distance2:
        return distance1
    else:
        return distance2
