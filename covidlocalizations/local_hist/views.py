from django.shortcuts import render
from localizator.models import LocalizationsData

def local_hist(response):	
	hist = LocalizationsData.objects.filter(name = response.user.username)	
	return render(response, 'local_hist/local_hist.html', {'output':history(hist)})
	
def history(hist):
	output = []
	for item in hist:
		for i in range(len(item.data["timelineObjects"])):
			if "activitySegment" in item.data["timelineObjects"][i]:
				output.append({"startTimeOfActivity" : item.data["timelineObjects"][i]["activitySegment"]["duration"]["startTimestampMs"]})
				output.append({"endTimeOfActivity" : item.data["timelineObjects"][i]["activitySegment"]["duration"]["endTimestampMs"]})
				output.append({"startLatitude" : item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["latitudeE7"]})
				output.append({"startLongitude" : item.data["timelineObjects"][i]["activitySegment"]["startLocation"]["longitudeE7"]})
				output.append({"endLatitude" : item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["latitudeE7"]})
				output.append({"endLongitude" : item.data["timelineObjects"][i]["activitySegment"]["endLocation"]["longitudeE7"]})
			else:
				output.append({"startTimeOfVisitingAPlace" : item.data["timelineObjects"][i]["placeVisit"]["duration"]["startTimestampMs"]})
				output.append({"endTimeOfVisitingAPlace" : item.data["timelineObjects"][i]["placeVisit"]["duration"]["endTimestampMs"]})
				output.append({"Place'sLatitude" : item.data["timelineObjects"][i]["placeVisit"]["location"]["latitudeE7"]})
				output.append({"Place'sLongitude" : item.data["timelineObjects"][i]["placeVisit"]["location"]["longitudeE7"]})
	return output
	
