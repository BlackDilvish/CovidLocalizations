from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_meetings, name="list_meetings"),
    path('contact/<str:lat1>/<str:lon1>/<str:lat2>/<str:lon2>', views.contact, name='contact'),
]
