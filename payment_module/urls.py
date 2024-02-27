from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('request', views.request_payment, name='request'),
    path('verify', views.verify_payment, name='verify_payment'),
]
