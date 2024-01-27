from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('course/<str:slug>', views.course_page, name='course'),
   path('my-courses/', views.my_courses, name='my_courses'),
]
