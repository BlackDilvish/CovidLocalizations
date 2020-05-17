from django.shortcuts import render
from list_meetings.views import get_contacts

divider = 1E7
precision = 7

def heatmap(response):
    username = response.user.username
    if response.method == 'POST':
        month = response.POST.get("choose_month") 
        year = response.POST.get("choose_year") 
        file_date = month + str(year)
        contacts = get_contacts(username, file_date)
        coordinates = get_coordinates(contacts)
        if len(coordinates):
            return render(response, 'heatmap/heatmap.html', {'mapid': 1, 
                                                        'name': username, 
                                                        'center': [50.067, 19.910], 
                                                        'localizations': coordinates})
    return render(response, 'heatmap/heatmap.html', {'name': username})


def get_coordinates(contacts):
    coordinates = []

    for contact in contacts:
        latitude = round(float(contact['location']['latitudeE7'] / divider), precision)
        longitude = round(float(contact['location']['longitudeE7'] / divider), precision)
        coordinates.append([latitude, longitude])

    return coordinates