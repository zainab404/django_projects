from django.shortcuts import render
from basicapp.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#^^^IMPORTS FOR LOGIN/LOGOUT FUNCTIONALITY


# Create your views here.
def index(request):
    return render(request, 'basicapp/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice job")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        #^^^we're passing in the user data that they inputted
        profile_form = UserProfileInfoForm(data=request.POST)

    
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            #^^^ this method hashes the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            #^^^this creates the one to one relationship with user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        
    return render(request, 'basicapp/registration.html', 
                        context={'user_form':user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #^^^Gets the username data from the user's login

        user = authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Inactive")
        else:
            print("User: " + "{}" + "login failure".format(username))
            return HttpResponse("Invalid Login Attempt")
    else:
        return render(request, 'basicapp/login.html', {})