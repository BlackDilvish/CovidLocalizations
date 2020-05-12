from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_meetings, name="local_hist"),
]
