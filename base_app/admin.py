from django.contrib import admin
from base_app.models import UserProfile, Project, Task, QuoteRequest

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(QuoteRequest)