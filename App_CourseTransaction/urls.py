from django.urls import path
from . import views 

urlpatterns = [
   path('course/<str:slug>', views.checkout_course , name='enroll_to_course'), 
]
