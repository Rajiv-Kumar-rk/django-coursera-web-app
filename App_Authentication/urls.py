from django.urls import path
from . import views

urlpatterns = [
   path('register/', views.user_registration, name='user_registration'),
   path('login', views.UserLoginView.as_view(), name='user_login'),
   path('logout/', views.user_logout, name='user_logout'),
   path('user-profile/', views.user_profile, name='user_profile'),
]
