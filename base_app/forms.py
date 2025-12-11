from django import forms
from django.contrib.auth.models import User
from base_app.models import UserProfile, QuoteRequest, Project, Task


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
    
class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
             if not instance.full_name:
                  user = instance.user
                  combined_name = f"{user.first_name} {user.last_name}".strip()
                  if combined_name:
                    self.fields['full_name'].initial = combined_name
    class Meta():
            model = UserProfile
            fields = (
            'full_name',        # <-- ADD THIS FIELD
            'company_name',     # <-- ADD THIS FIELD
            'phone_number', 
            'business_type', 
            'profile_pic'
        )
class UserUpdateForm(forms.ModelForm):
    # Makes sure the email field is pulled from the User model and is visible
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        # Include first_name, last_name, and email to update standard user info
        fields = ('first_name', 'last_name', 'email')
class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ('client_name', 'client_email', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }