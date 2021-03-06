# [Covid localizations]
[![Coverage Status](https://coveralls.io/repos/github/BlackDilvish/CovidLocalizations/badge.png?branch=master)](https://coveralls.io/github/BlackDilvish/CovidLocalizations?branch=master)
## Participants 
- [Gabriel Naleźnik](https://github.com/BlackDilvish) - team leader
- [Olga Kubiszyn](https://github.com/olgaaaglo)
- [Wojciech Gomułka](https://github.com/Excavelty)
- [Jan Zajda](https://github.com/Grzybiarz47)
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
- Displaying your nearest distance from an infected person
- Displaying dangerous localizations in leaflet maps widget 

## Screenshots:

- Home page
<img src=".\covidlocalizations\static\home.png" width="800"/>

- Dark mode
<img src=".\covidlocalizations\static\darkmode.png" width="800"/>

- History of user's localizations
<img src=".\covidlocalizations\static\lochist.png" width="800"/>

- Table of contacts with infected people
<img src=".\covidlocalizations\static\contacttab.png" width="800"/>

- Information about possible contact
<img src=".\covidlocalizations\static\contactinfo.png" width="800"/>

- Heatmap with possibly infected places
<img src=".\covidlocalizations\static\heatmap1.png" width="800"/>

- Heatmap with places where the user was and where he had contact with infected people
<img src=".\covidlocalizations\static\heatmap2.png" width="800"/>

## Technologies:
- Django
- Leaflet an open-source JavaScript library for mobile-friendly interactive maps (https://leafletjs.com/examples.html)
- Google Takeout for localization data (https://takeout.google.com)

## Advanced project description:
- Product backlog on Trello: https://trello.com/b/25mkJJVa/covid-localizations
- Go to our website: https://covidlocalizations.herokuapp.com

### Week 1 (27.04-03.05):
- Basic web page
- Adding models to database
- Parsing json with user’s localizations

### Week 2 (04.05-10.05):
- Create server
- Basic user registration
- Infected status
- Saving data to database
- Showing localizations on map widget
- History of localizations

### Week 3 **[half of the deadline]** (11.05-17.05):
- Displaying distance to potentially infected places
- Displaying board of close contacts with infected people (distance, localization, possible vehicle used by user and infected person etc.)

### Week 4 (18.05-24.05):
- Sending notifications about possible meeting with infected person
- Heatmap of user's localizations

### Week 5 (25.05-31.05):
- Calculating position of the nearest infected person
- Calculating possibility of being infected based on the vehicle you were using and how much time you spent with infected person - information displayed as part of board of close contacts
- Displaying infected places on a heatmap

### Week 6  (01.06-07.06):
- Advanced web page (design)
- Displaying places where the user met an infected person

### Week 7  (08.06-14.06):
- Writing unittests for 95% of the code
- Finishing previous tasks if obstacles are met

### Week 8 **[finish]**  (15.06-17.06):
- Last bugfixes before a deadline
- *celebrating* \o/


