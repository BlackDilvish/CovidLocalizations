from django.urls import path
from . import views

urlpatterns = [
    path('', views.local_hist, name="local_hist"),
    path('visit/<int:lat>/<int:long>', views.visit, name="visit"),
    path('activity/<int:lat1>/<int:long1>/<int:lat2>/<int:long2>', views.activity, name="activity"),
]