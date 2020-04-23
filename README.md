# [CovidInfoOnline]
## Participants 
- Gabriel Naleźnik - team leader
- Olga Kubiszyn
- Wojciech Gomułka
- Jan Zajda
### Do you need more people: No
## Short description of the idea:
CovidInfoOnline is web app that processes data about Covid19. You can choose country and display corresponding charts describing data like number of cases, deaths, recovered 
or conducted tests. Moreover you can compare selected countries. It will have many additional features, such as:

## Features:
- search bar allowing seeking for data by city name/country
- displaying general data among different countries/cities on charts
- short info about countries (population, etc.)
- red bar with info from https://www.gov.pl/web page
- predicting future cases, deaths and recovered with machine learning algorithms
- saving predicted data in files ( *.txt, *.csv, *.json )
- displaying number of tests among countries
- showing correlation between daily new confirmed cases and sunny weather (Do people stay at home?)
- displaying ”N” countries with most confirmed/deaths/recovered
- checking if you have covid symptoms and your mood in correlation to covid statistics ( quiz!)
- displaying percent number of patients having given symptom
- tips, how to avoid being infected

## Technologies:
- Django
- Tensorflow (For predicting future cases)
- Covid data from - Novel Coronavirus (COVID-19) Cases, provided by JHU CSSE (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)
- Description about countries from api: https://restcountries.eu/#api-endpoints-name

