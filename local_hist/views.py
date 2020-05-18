from django.shortcuts import render
from localizator.models import LocalizationsData
from django.http import HttpResponse
from datetime import datetime


def local_hist(response):
	username = response.user.username
	file_date = ""

	if response.method == "POST":
		month = response.POST.get("choose_month")
		year = response.POST.get("choose_year")
		file_date = month + str(year)

	hist = LocalizationsData.objects.filter(name=username, file_date=file_date)

	if len(hist):
		out = history(hist)
		return render(response, 'local_hist/local_hist.html', {'name': username, 'output': convert(out)})
	return render(response, 'local_hist/local_hist.html', {'name': username})


def visit(response, lat, lon):
	username = response.user.username
	return render(response, 'local_hist/local_map.html', {'mapid': "mapid", 'lat1': lat,
															'lon1': lon, 'name': username})


def activity(response, lat1, lon1, lat2, lon2):
	username = response.user.username
	return render(response, 'local_hist/local_map.html', {'mapid': "mapid", 'lat1': lat1,
															'lon1': lon1, 'lat2': lat2,
															'lon2': lon2, 'name': username})		  	


def history(hist):
	output = []
	
	for item in hist:
		for i in range(len(item.data["timelineObjects"])):
			if "activitySegment" in item.data["timelineObjects"][i]:
				output.append(item_activity(item, i))
			else:
				output.append(item_visit(item, i))
	return output


def convert(output):
	for item in output:
		for key, val in item.items():
			if key == "Start_time" or key == "End_time":
				item[key] = datetime.utcfromtimestamp(int(val)/1000)
			elif isinstance(val, int):
				item[key] = str(float(val)/10e6)
	return output

		
def item_activity(item, i):
	act = {}	
	data = item.data["timelineObjects"][i]["activitySegment"]	

	if "duration" in data and "startTimestampMs" in data["duration"]:
		act["Start_time"] = data["duration"]["startTimestampMs"]

	if "duration" in data and "endTimestampMs" in data["duration"]:  
		act["End_time"] = data["duration"]["endTimestampMs"]
		
	if "startLocation" in data and "latitudeE7" in data["startLocation"]: 
		act["Start_latitude"] = data["startLocation"]["latitudeE7"]
	
	if "startLocation" in data and "longitudeE7" in data["startLocation"]: 
		act["Start_longitude"] = data["startLocation"]["longitudeE7"]
	
	if "endLocation" in data and "latitudeE7" in data["endLocation"]: 
		act["End_latitude"] = data["endLocation"]["latitudeE7"]
	
	if "endLocation" in data and "longitudeE7" in data["endLocation"]: 
		act["End_longitude"] = data["endLocation"]["longitudeE7"]
	
	if "distance" in data:
		act["Distance"] = str(data["distance"])

	if "activityType" in data:
		act["Activity_type"] = data["activityType"]
	
	if "activities" in data and "probability" in data["activities"][0]:
		act["Probability"] = data["activities"][0]["probability"]

	return act


def item_visit(item, i):
	vis = {}
	data = item.data["timelineObjects"][i]["placeVisit"]

	if "duration" in data and "startTimestampMs" in data["duration"]:
		vis["Start_time"] = data["duration"]["startTimestampMs"]
	
	if "duration" in data and "endTimestampMs" in data["duration"]:
		vis["End_time"] = data["duration"]["endTimestampMs"]
	
	if "location" in data and "latitudeE7" in data["location"]:
		vis["Places_latitude"] = data["location"]["latitudeE7"]
	
	if "location" in data and "longitudeE7" in data["location"]:
		vis["Places_longitude"] = data["location"]["longitudeE7"]
	
	if "location" in data and "address" in data["location"]:
		vis["Address"] = data["location"]["address"]
	
	if "location" in data and "locationConfidence" in data["location"]:
		vis["Location_confidence"] = data["location"]["locationConfidence"]

	if "visitConfidence" in data:
		vis["Visit_confidence"] = float(data["visitConfidence"]) 

	return vis
