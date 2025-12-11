from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


#LOGIN
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from base_app import models
from .models import Project, Task, QuoteRequest, UserProfile

from base_app.forms import UserForm, UserProfileForm, UserUpdateForm, QuoteRequestForm
# Create your views here.
class IndexView(TemplateView):
    """Handles the home page."""
    template_name = 'base_app/index.html'
class AboutView(TemplateView):
    template_name = 'base_app/about.html'



class RegisterView(FormView):
    template_name = 'base_app/registration.html'
    success_url = reverse_lazy('base_app:profile_detail')

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
            return reverse_lazy('base_app:profile_detail')
            
        return url
class UserLogoutView(AuthLogoutView):
    next_page = reverse_lazy('base_app:index')

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'base_app/profile_detail.html'

    def get_object(self, queryset=None):
        return self.request.user.userprofile
class UserProfileUpdateView(LoginRequiredMixin, View):
    model = UserProfile
    success_url = reverse_lazy('base_app:profile_detail')
    template_name = 'base_app/profile_update.html'

    def get_forms(self, user_data=None, profile_data=None, files=None):       
        user = self.request.user
        profile = user.userprofile

        profile_initial_data = {}
        
        if not user_data and not profile.full_name:
            combined_name = f"{user.first_name} {user.last_name}".strip()
            if combined_name:
                profile_initial_data['full_name'] = combined_name
        
        user_form = UserUpdateForm(user_data, instance=user)
        profile_form = UserProfileForm(
            profile_data, 
            files, 
            instance=profile, 
            initial=profile_initial_data # <-- This ensures pre-population
        )

        return user_form, profile_form

    def get(self, request, *args, **kwargs):
        user_form, profile_form = self.get_forms()
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form, profile_form = self.get_forms(
            user_data=request.POST,
            profile_data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            return redirect(self.success_url)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)

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
    
class GetQuoteView(LoginRequiredMixin, CreateView): # ADD LoginRequiredMixin
    model = QuoteRequest
    form_class = QuoteRequestForm
    template_name = 'base_app/quote_request.html'
    success_url = reverse_lazy('base_app:quote_history') # BETTER UX: Redirect to history instead of index

    def get_initial(self):
        initial = super().get_initial()
        # Access the logged-in user and their profile
        user = self.request.user
        profile = user.userprofile
        # Map the user/profile data to the QuoteRequest form fields
        initial['client_name'] = profile.full_name or user.get_full_name() or user.username
        initial['client_email'] = user.email
        initial['client_phone'] = profile.phone_number

        # Check if the fields are filled from the profile, if not, use the User model's data
        if not initial['client_name'] and user.first_name and user.last_name:
            initial['client_name'] = f"{user.first_name} {user.last_name}"
            
        return initial
    
    def form_valid(self, form):
        # 1. Take the object from the form, but DO NOT save it yet (commit=False)
        self.object = form.save(commit=False)
        
        # 2. **CRITICAL FIX:** Assign the logged-in user before saving
        self.object.user = self.request.user
        
        # 3. Now save the instance with the user assigned
        self.object.save()
        
        # 4. Return the standard CreateView success response
        return super().form_valid(form)

class QuoteHistoryView(LoginRequiredMixin, ListView):
    """Displays a list of all QuoteRequests made by the logged-in user."""
    model = QuoteRequest
    template_name = 'base_app/quote_history.html'
    context_object_name = 'quotes' # Will be used to iterate in the template

    def get_queryset(self):
        # Crucial step: Filter the QuoteRequests to show only those belonging 
        # to the currently logged-in user.
        return QuoteRequest.objects.filter(user=self.request.user).order_by('-submission_date')
    
class QuoteDeleteView(LoginRequiredMixin, DeleteView):
    model = QuoteRequest
    success_url = reverse_lazy('base_app:quote_history')
    template_name = 'base_app/quote_confirm_delete.html'
    def get_queryset(self):
        return QuoteRequest.objects.filter(user=self.request.user)