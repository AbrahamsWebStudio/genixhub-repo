from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #Additional classes
    phone_number = models.CharField(max_length=20, blank=True, default="+254")

    business_type = models.CharField(max_length=150, blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics' , blank=True)

    def __str__(self):
        return self.user.username
