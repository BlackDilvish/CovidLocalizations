from django.shortcuts import render
from localizator.models import LocalizationsData
from django.http import HttpResponse
from datetime import datetime

def local_hist(response):
	username = response.user.username	
	hist = LocalizationsData.objects.filter(name = username)
	out = history(hist)
	return render(response, 'local_hist/local_hist.html', {'name': username, 'output': convert(out)})

def visit(response, lat, lon):
	username = response.user.username
	return render(response, 'local_hist/local_map.html', {'lat1': lat,'lon1': lon, 'name': username})

def activity(response, lat1, lon1, lat2, lon2):
	username = response.user.username
	return render(response, 'local_hist/local_map.html', {'lat1': lat1,'lon1': lon1, 
								'lat2': lat2,'lon2': lon2,
     							  	'name': username})

def history(hist):
	output = []
	for item in hist:
		for i in range(len(item.data["timelineObjects"])):
			if "activitySegment" in item.data["timelineObjects"][i]:
				act = {}
				
				act["Start_time"] = item.data["timelineObjects"][i]["activitySegment"]["duration"]["startTimestampMs"]
				
				act["End_time"] = item.data["timelineObjects"][i]["activitySegment"]["duration"]["endTimestampMs"]
				 
				act["Start_latitude"] = item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["latitudeE7"]
				
				act["Start_longitude"] = item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["longitudeE7"]
				
				act["End_latitude"] = item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["latitudeE7"]
				
				act["End_longitude"] = item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["longitudeE7"]
				
				act["Distance"] = str(item.data["timelineObjects"][i]["activitySegment"]["distance"]) #string zeby nie konwertowalo na wspolrzedne
				
				act["Activity_type"] = item.data["timelineObjects"][i]["activitySegment"]["activityType"]
				
				act["Probability"] = item.data["timelineObjects"][i]["activitySegment"]["activities"][0]["probability"]
				
				output.append(act)
			else:
				vis = {}
				
				vis["Start_time"] = item.data["timelineObjects"][i]["placeVisit"]["duration"]["startTimestampMs"]
				
				vis["End_time"] = item.data["timelineObjects"][i]["placeVisit"]["duration"]["endTimestampMs"]
				
				vis["Places_latitude"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["latitudeE7"]
				
				vis["Places_longitude"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["longitudeE7"]
				
				vis["Address"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["address"]
				
				vis["Location_confidence"] = item.data["timelineObjects"][i]["placeVisit"]["location"]["locationConfidence"]
				
				vis["Visit_confidence"] = float(item.data["timelineObjects"][i]["placeVisit"]["visitConfidence"]) 
				
				output.append(vis)
	return output
	
def convert(output):
	for item in output:
		print(item)
		for key, val in item.items():
			if key == "Start_time" or key == "End_time":
				item[key] = datetime.utcfromtimestamp(int(val)/1000)
			elif isinstance(val, int):
				item[key] = str(float(val)/10e6) #na stringa zeby mapa dzialala
	return output
		
	
