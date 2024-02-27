from django.urls import path
from . import views
app_name = 'events'

urlpatterns = [
    path('', views.EventsList.as_view(), name='events'),
    path('events/<pk>', views.event_detail, name='detail'),
    path('register/<pk>', views.register_event, name='register'),
    path('card', views.card, name='card')
]