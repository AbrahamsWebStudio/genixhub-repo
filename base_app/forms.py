from django import forms
from django.contrib.auth.models import User
from base_app.models import UserProfile, QuoteRequest


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
    
class UserProfileForm(forms.ModelForm):
        class Meta():
            model = UserProfile
            fields = ('phone_number','business_type', 'profile_pic')

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ('client_name', 'client_email', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }