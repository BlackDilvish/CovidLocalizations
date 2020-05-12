from django.shortcuts import render
from localizator.models import LocalizationsData
from django.http import HttpResponse
from datetime import datetime

def local_hist(response):
	username = response.user.username
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	years = [2019, 2020]
	file_date = ""

	if response.method == "POST":
		month = response.POST.get("choose_month")
		year = response.POST.get("choose_year")
		file_date = month + str(year)

	hist = LocalizationsData.objects.filter(name=username, file_date=file_date)
	if len(hist):
		out = history(hist)
		return render(response, 'local_hist/local_hist.html', {'name': username, 'output': convert(out), "months": months, "years": years})
	return render(response, 'local_hist/local_hist.html', {'name': username, "months": months, "years": years})


def visit(response, lat, lon):
	username = response.user.username
	return render(response, 'local_hist/local_map.html', {'mapid': "mapid", 'lat1': lat,'lon1': lon, 'name': username})


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
	if "duration" in item.data["timelineObjects"][i]["activitySegment"] and "startTimestampMs" in item.data["timelineObjects"][i]["activitySegment"]["duration"]:
		act["Start_time"] = item.data["timelineObjects"][i]["activitySegment"]["duration"]["startTimestampMs"]

	if "duration" in item.data["timelineObjects"][i]["activitySegment"] and "endTimestampMs" in item.data["timelineObjects"][i]["activitySegment"]["duration"]:  
		act["End_time"] = item.data["timelineObjects"][i]["activitySegment"]["duration"]["endTimestampMs"]
		
	if "startLocation" in item.data["timelineObjects"][i]["activitySegment"] and "latitudeE7" in item.data["timelineObjects"][i]["activitySegment"]["startLocation"]: 
		act["Start_latitude"] = item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["latitudeE7"]
	
	if "startLocation" in item.data["timelineObjects"][i]["activitySegment"] and "longitudeE7" in item.data["timelineObjects"][i]["activitySegment"]["startLocation"]: 
		act["Start_longitude"] = item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["longitudeE7"]
	
	if "endLocation" in item.data["timelineObjects"][i]["activitySegment"] and "latitudeE7" in item.data["timelineObjects"][i]["activitySegment"]["endLocation"]: 
		act["End_latitude"] = item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["latitudeE7"]
	
	if "endLocation" in item.data["timelineObjects"][i]["activitySegment"] and "longitudeE7" in item.data["timelineObjects"][i]["activitySegment"]["endLocation"]: 
		act["End_longitude"] = item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["longitudeE7"]
	
	if "distance" in item.data["timelineObjects"][i]["activitySegment"]:
		act["Distance"] = str(item.data["timelineObjects"][i]["activitySegment"]["distance"])
	if "activityType" in item.data["timelineObjects"][i]["activitySegment"]:
		act["Activity_type"] = item.data["timelineObjects"][i]["activitySegment"]["activityType"]
	
	if "activities" in item.data["timelineObjects"][i]["activitySegment"] and "probability" in item.data["timelineObjects"][i]["activitySegment"]["activities"][0]:
		act["Probability"] = item.data["timelineObjects"][i]["activitySegment"]["activities"][0]["probability"]

	return act


def item_visit(item, i):
	vis = {}
				
	if "duration" in item.data["timelineObjects"][i]["placeVisit"] and "startTimestampMs" in item.data["timelineObjects"][i]["placeVisit"]["duration"]:
		vis["Start_time"] = item.data["timelineObjects"][i]["placeVisit"]["duration"]["startTimestampMs"]
	
	if "duration" in item.data["timelineObjects"][i]["placeVisit"] and "endTimestampMs" in item.data["timelineObjects"][i]["placeVisit"]["duration"]:
		vis["End_time"] = item.data["timelineObjects"][i]["placeVisit"]["duration"]["endTimestampMs"]
	
	if "location" in item.data["timelineObjects"][i]["placeVisit"] and "latitudeE7" in item.data["timelineObjects"][i]["placeVisit"]["location"]:
		vis["Places_latitude"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["latitudeE7"]
	
	if "location" in item.data["timelineObjects"][i]["placeVisit"] and "longitudeE7" in item.data["timelineObjects"][i]["placeVisit"]["location"]:
		vis["Places_longitude"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["longitudeE7"]
	
	if "location" in item.data["timelineObjects"][i]["placeVisit"] and "address" in item.data["timelineObjects"][i]["placeVisit"]["location"]:
		vis["Address"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["address"]
	
	if "location" in item.data["timelineObjects"][i]["placeVisit"] and "locationConfidence" in item.data["timelineObjects"][i]["placeVisit"]["location"]:
		vis["Location_confidence"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["locationConfidence"]
	
	if "visitConfidence" in item.data["timelineObjects"][i]["placeVisit"]:
		vis["Visit_confidence"] = float(item.data["timelineObjects"][i]["placeVisit"]["visitConfidence"]) 

	return vis
