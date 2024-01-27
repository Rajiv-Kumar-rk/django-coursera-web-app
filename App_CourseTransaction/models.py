from django.db import models
from django.contrib.auth.models import User
from App_Course.models import Course
# Create your models here.

class UserCourse(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " -- purchased --> " + self.course.name


class Payment(models.Model):
    user_course = models.ForeignKey(UserCourse, null=True, blank=True, on_delete=models.CASCADE) #to add only those specific data with successful payment 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, null=False)
    payment_id = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return "Order_id: " + self.order_id 
