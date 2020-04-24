# [Covid localizations]
## Participants 
- Gabriel Naleźnik - team leader
- Olga Kubiszyn
- Wojciech Gomułka
- Jan Zajda
### Do you need more people: No

## Short description of the idea:
Covid localizations is web app that checks if you were near someone infected. You can load information about your locations from previous months and compare it with locations from infected people. You can also check potentially dangerous places close to your current position.
 		
## Features:
- User registration
- Saving user’s localization history in database and checking if he had any contact with infected person (no automation in version 1.0, json has to be given by user, we will think of automating later)
- User can set since when he is infected
- Displaying probability if user was traveling by foot or using some type of vehicle 
(e.g.: if user was travelling by bus he could have bigger chance to become infected)
- Notifications (emails) with information about probable meeting with infected person in the past
- Daily tips: how to avoid being infected!
- Displaying your nearest distance from an infected person
- Displaying dangerous localizations in leaflet maps widget 

## Technologies:
- Django
- Leaflet an open-source JavaScript library for mobile-friendly interactive maps (https://leafletjs.com/examples.html)
- Google Takeout for localization data (https://takeout.google.com)

