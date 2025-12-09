from django.shortcuts import render
from base_app.forms import UserForm, UserProfileForm



#LOGIN
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'base_app/index.html')

def about(request):
    return render(request, 'base_app/about.html')

@login_required
def services(request):
    return render(request, 'base_app/services.html')

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False) 
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

                profile.save()

                registered = True
            else:
                print("User Form Errors:", user_form.errors)
                print("Profile Form Errors:", profile_form.errors)
                return render(request, 'base_app/registration.html', 
                          {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'base_app/registration.html', 
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered
                      
                  }
                  )

def user_login(request):

    if request.method == "POST":
        username =request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                
                next_url = request.POST.get('next') or request.GET.get('next')

                if next_url:
                    # Redirect user back to the page they were originally trying to access
                    return HttpResponseRedirect(next_url)
                else:
                    # If no 'next' parameter, redirect to the default index page
                    return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Is Not Active!")
        else:
            print("Login Using the correct Methods")
            return HttpResponse("Invalid Login Details...")
    else:
        return render(request, 'base_app/login.html', {})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
