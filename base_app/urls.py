from django.urls import path
from base_app import views
from .views import (
    IndexView, AboutView, RegisterView, ServiceListView, ProjectDetailView,
    UserLoginView, UserLogoutView, GetQuoteView, UserProfileUpdateView, UserProfileDetailView, QuoteHistoryView, QuoteDeleteView,
)

app_name = 'base_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'), 
    path('about/', AboutView.as_view(), name='about'),

    path('register/', RegisterView.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),

    path("profile_detail/", UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile_update/', UserProfileUpdateView.as_view(), name='profile_update'),


    path("services/", ServiceListView.as_view(),name='services'),
    path('services/<int:pk>/', ProjectDetailView.as_view(), name='project'),

    path('quote/', GetQuoteView.as_view(), name='get_quote'),
    path('quote_history/', views.QuoteHistoryView.as_view(), name='quote_history'),
    path('quote_delete/<int:pk>/', QuoteDeleteView.as_view(), name='quote_delete'),
    
]
    
    