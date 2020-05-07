from django.shortcuts import render
from localizator.models import LocalizationsData
from django.http import HttpResponse

def local_hist(response):
	username = response.user.username	
	hist = LocalizationsData.objects.filter(name = username)	
	return render(response, 'local_hist/local_hist.html', {'name': username, 'output': history(hist)})

def visit(response, lat, long):
	username = response.user.username
	return render(response, 'local_hist/local_map.html', {'lat1': float(lat)/10e6,'long1': float(long)/10e6, 
														  'name': username})

def activity(response, lat1, long1, lat2, long2):
	username = response.user.username
	return render(response, 'local_hist/local_map.html', {'lat1': float(lat1)/10e6,'long1': float(long1)/10e6, 
														  'lat2': float(lat2)/10e6,'long2': float(long2)/10e6,
														  'name': username})

def history(hist):
	output = []
	for item in hist:
		for i in range(len(item.data["timelineObjects"])):
			if "activitySegment" in item.data["timelineObjects"][i]:
				act = {}
				act["startTimeOfActivity"] = item.data["timelineObjects"][i]["activitySegment"]["duration"]["startTimestampMs"]
				act["endTimeOfActivity"] = item.data["timelineObjects"][i]["activitySegment"]["duration"]["endTimestampMs"]
				act["startLatitude"] = item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["latitudeE7"]
				act["startLongitude"] = item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["longitudeE7"]
				act["endLatitude"] = item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["latitudeE7"]
				act["endLongitude"] = item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["longitudeE7"]
				output.append(act)
			else:
				vis = {}
				vis["startTimeOfVisitingAPlace"] = item.data["timelineObjects"][i]["placeVisit"]["duration"]["startTimestampMs"]
				vis["endTimeOfVisitingAPlace"] = item.data["timelineObjects"][i]["placeVisit"]["duration"]["endTimestampMs"]
				vis["PlacesLatitude"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["latitudeE7"]
				vis["PlacesLongitude"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["longitudeE7"]
				output.append(vis)
	return output
	
