from django.shortcuts import render, redirect
from base_app.forms import UserForm, UserProfileForm
from base_app import models
from .models import Project, Task, QuoteRequest
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

#LOGIN
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from .forms import UserForm, UserProfileForm, QuoteRequestForm

# Create your views here.
class IndexView(TemplateView):
    """Handles the home page."""
    template_name = 'base_app/index.html'

class AboutView(TemplateView):
    template_name = 'base_app/about.html'

class RegisterView(FormView):
    template_name = 'base_app/registration.html'
    success_url = reverse_lazy('base_app:index')

    def get_form(self, form_class=None):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserForm()
        if 'profile_form' not in context:
            context['profile_form'] = UserProfileForm()
            
        context['registered'] = False
        return context
    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            return self.form_invalid(user_form, profile_form)
    def form_valid(self, user_form, profile_form):
        # 1. Save User
        user = user_form.save()
        user.set_password(user.password) # Hash the password
        user.save()
        # 2. Save Profile (linking to the new User)
        profile = profile_form.save(commit=False)
        profile.user = user
        # 3. Handle File Upload
        if 'profile_pic' in self.request.FILES:
            profile.profile_pic = self.request.FILES['profile_pic']

        profile.save()
        # Return success redirect
        return redirect(self.success_url)
    
    def form_invalid(self, user_form, profile_form):
        # This ensures the template re-renders with the user's input and error messages
        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form,
            registered=False
        )
        return self.render_to_response(context)

class UserLoginView(AuthLoginView):

    template_name = 'base_app/login.html'
    redirect_field_name = 'next'

    def get_success_url(self):
        url = super().get_success_url()
        if url == self.request.path:
            return reverse_lazy('base_app:index')
            
        return url
class UserLogoutView(AuthLogoutView):
    next_page = reverse_lazy('base_app:index')




#Projects View --Displays a list of all active projects, used here to showcase services
class ServiceListView(ListView):
    model = Project
    template_name = 'base_app/services.html' # We will create this file next
    context_object_name = 'projects' # The variable name to use in the template
    
    # Optionally filter to only show completed/public projects
    def get_queryset(self):
        return Project.objects.filter(status__in=['C', 'I']).order_by('-start_date') 
        # C: Completed, I: In Progress (to show active work)

class ProjectDetailView(DetailView):
    """
    Displays the details of a single Project (used as a Service Case Study)
    along with all its associated tasks.
    """
    model = Project
    template_name = 'base_app/project_detail.html'
    context_object_name = 'project' # The object will be accessible as 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all tasks related to this project to the context
        context['tasks'] = self.object.tasks.all().order_by('due_date')
        return context
class GetQuoteView(CreateView):
    model = QuoteRequest
    form_class = QuoteRequestForm
    template_name = 'base_app/quote_request.html'
    success_url = reverse_lazy('base_app:index')
    