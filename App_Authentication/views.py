from django.shortcuts import render, redirect
from App_Authentication.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail #library
# Create your views here.

def user_registration(request): 
    if request.user.is_authenticated:
        return redirect('home')
    
    elif request.method == 'GET':
        registration_form = UserRegistrationForm()

        data = {
            'registration_form' : registration_form,
        }
        return render(request, 'App_Authentication/registration_page.html', context=data)
    
    elif request.method == 'POST':
        registration_form = UserRegistrationForm(data = request.POST)

        register_status = False

        if registration_form.is_valid():    
            registration_form.save()
            register_status = True

            #sending mail on successful registration to the user
            mail_message_body = 'Thank you {0}, on successful registration of yourself with us! Yours registered details : (Username : {1}, Email Id : {2}). Login to Website for more details- http://localhost:8000/account/login'.format(request.POST.get('first_name'), request.POST.get('username'), request.POST.get('email'))
            mail_receiver_address = request.POST.get('email')
            send_mail(
                'Registration Successful with Us(Skill Gliding)', #subject of mail here
                mail_message_body, #content or body of mail here
                'skillgliding@gmail.com', #sender's mail address here
                [mail_receiver_address], #receiver's mail address here
                fail_silently=False
            )

        data = {
        'registration_form' : registration_form,
        'register_status' : register_status,
        }

        return render(request, 'App_Authentication/registration_page.html', context=data)   


class UserLoginView(View):
    def get(self, request):
        login_form = UserLoginForm()

        data = {
            'login_form' : login_form
        }
        return render(request, 'App_Authentication/login_page.html', context=data)
    
    def post(self, request):
        login_form = UserLoginForm(request, data=request.POST)

        if login_form.is_valid():
            #implementation of authenticating the user object is done in forms.py 'UserLoginForm'
            next_page = request.GET.get('next')
            #print("next page: ", next_page)
            if next_page is not None:
                return redirect(next_page)
            else:
                return redirect('home')

        data = {
            'login_form' : login_form
        }
        return render(request, 'App_Authentication/login_page.html', context=data)

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def user_profile(request):
    data = {
        'user' : request.user
    }
    return render(request, 'App_Authentication/user_profile.html', context=data)