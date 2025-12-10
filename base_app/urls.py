from django.urls import path
from base_app import views
from .views import (
    IndexView, AboutView, RegisterView, ServiceListView, ProjectDetailView,
    UserLoginView, UserLogoutView, GetQuoteView
)

app_name = 'base_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'), 
    path('about/', AboutView.as_view(), name='about'),

    path('register/', RegisterView.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),

    path("services/", ServiceListView.as_view(),name='services'),
    path('services/<int:pk>/', ProjectDetailView.as_view(), name='project'),
    path('quote/', GetQuoteView.as_view(), name='get_quote'),

]

