from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_meetings, name="list_meetings"),
    path('contact/<str:lat1>/<str:lon1>/<str:lat2>/<str:lon2>/<str:inf_act>/<str:user_act>/<int:near>/<int:duration>', views.contact, name='contact'),
    path('external/<str:lat1>/<str:lon1>/<str:lat2>/<str:lon2>/<str:inf_act>/<str:user_act>/<int:near>/<int:duration>', views.external, name='external')
]
