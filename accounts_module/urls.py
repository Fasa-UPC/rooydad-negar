from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_user, name='logout')

]
