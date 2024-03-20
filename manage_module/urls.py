from django.urls import path
from . import views

app_name  = "manage"

urlpatterns = [
    path('users', views.ManageUser.as_view(), name='users'),
    path('user/<pk>', views.UserDetail.as_view(), name='user'),
    path('field/<pk>', views.user_info_by_field, name='user_info_field'),
    path('events', views.ManageEvents.as_view(), name='events'),
    path('event/<pk>', views.ShowEventsInfo.as_view(), name='show_event'),
    path('event/state/<pk>', views.download_event_state, name='download_event'),
    path('cancel/<event>/<user>', views.cancel_event, name='cancel_event')
]