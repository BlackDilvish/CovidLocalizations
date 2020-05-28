from django.urls import path
from . import views

urlpatterns = [
    path('', views.local_hist, name="local_hist"),
    path('visit/<str:lat>/<str:lon>', views.visit, name="visit"),
    path('activity/<str:lat1>/<str:lon1>/<str:lat2>/<str:lon2>', views.activity, name="activity"),
]
