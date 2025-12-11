from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse, reverse_lazy
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ADDED FIELDS
    full_name = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True) 
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.full_name or self.user.username

#CBV & LBV
# --- CHOICES FOR PROJECT STATUS ---
PROJECT_STATUS_CHOICES = (
    ('P', 'Planning'),
    ('I', 'In Progress'),
    ('R', 'Review'),
    ('H', 'On Hold'),
    ('C', 'Completed'),
)

# --- CHOICES FOR TASK STATUS & PRIORITY ---
TASK_STATUS_CHOICES = (
    ('TD', 'To Do'),
    ('IP', 'In Progress'),
    ('QA', 'Awaiting Review'),
    ('DO', 'Done'),
)

TASK_PRIORITY_CHOICES = (
    ('L', 'Low'),
    ('M', 'Medium'),
    ('H', 'High'),
    ('C', 'Critical'),
)


# =========================================================
# 1. Project Model
# =========================================================

class Project(models.Model):
    # Core Fields
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    client = models.CharField(max_length=150)

    # Date/Time and Status Fields
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    
    # Financials (using DecimalField for accurate money tracking)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(
        max_length=1, 
        choices=PROJECT_STATUS_CHOICES, 
        default='P'
    )

    # Relationships
    # ForeignKey to the Django User model for the project manager
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='managed_projects'
    )
    
    # Audit Field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
    def get_absolute_url(self):
        return reverse("base_app:project", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['due_date']
    
class Task(models.Model):
    # Relationships (The one-to-many link)
    # If a Project is deleted, all associated Tasks are deleted (models.CASCADE)
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks' # Allows you to access all tasks from a project: project.tasks.all()
    )
    
    # ForeignKey to the Django User model for the assignee
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks'
    )

    # Core Fields
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    # Date/Time and Status Fields
    due_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(
        max_length=2, 
        choices=TASK_STATUS_CHOICES, 
        default='TD'
    )

    # Priority
    priority = models.CharField(
        max_length=1, 
        choices=TASK_PRIORITY_CHOICES, 
        default='M'
    )
    
    # Estimation (Using IntegerField for hours)
    estimated_time = models.IntegerField(default=0, help_text="Estimated time in hours")

    def __str__(self):
        return f"{self.project.name}: {self.title} ({self.get_priority_display()})"

    class Meta:
        ordering = ['due_date', 'priority']

#Quote Request
class QuoteRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quote_requests', null=True, blank=True)  
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    description = models.TextField(help_text="Describe the service you need.")
    submission_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Quote Request from {self.client_name}"

    class Meta:
        verbose_name_plural = "Quote Requests"