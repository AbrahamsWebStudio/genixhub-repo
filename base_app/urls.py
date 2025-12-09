from django.urls import path
from base_app import views

app_name = 'base_app'

urlpatterns = [
    path('', views.index, name='index'),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"), 
    path("registration/", views.register, name="register"), 
    path("User_login/", views.user_login, name="user_login"),  
]

