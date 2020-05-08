from django.urls import path
from . import views

urlpatterns = [
    path('', views.instruction, name="instruction"),
    path('instruction', views.instruction, name="instruction"),
    path('home', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    path('status', views.status, name='status'),
]