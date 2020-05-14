from django.shortcuts import render

def index(response):
    username = response.user.username
    locs = [ [50.33623, 19.215649],
             [50.33629, 19.215689],
             [50.33689, 19.225649],
             [50.33629, 19.215849],
             [50.33689, 19.215649],
             [50.33629, 19.218649],
             [50.33229, 19.215649],
             [50.33829, 19.215649],
    ]

    return render(response, 'heatmap/index.html', {'mapid': 1, 
                                                'name': username, 
                                                'center': [50.336, 19.215], 
                                                'localizations': locs})
