from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ValidationError
from django.contrib.auth import authenticate, login
 
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    email = forms.EmailField(label='Email Address', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Password Confirmation', required=True)

    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = None
        try:
            user = User.objects.get(email = email)
        except:
            return email
        
        if user is not None:
            raise ValidationError("User with the same email address already Exist!")


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email Address' , required=True) 
    #converting username field to email field on webpage, so that we can login the user with 'email' as username and password
    #after, taking email in username , we will handle the other work like fetching correct user to respective email address from database 'User'
    
    def clean(self):
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        user = None
        
        try:
            user = User.objects.get(email=email)
            result_user = authenticate(username=user.username, password=password)

            if result_user is not None:
                login(self.request, result_user)
                return result_user
            else:
                raise ValidationError("Email Address or Password is Invalid!")

        except:
            raise ValidationError("Email Address or Password is Invalid!")
        