from django.db import models

# Create your models here. 
class Course(models.Model):
    name = models.CharField(max_length=100, null=False)
    slug = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500, null=True)
    banner_pic = models.ImageField(upload_to='course_banner_pics')
    creation_date = models.DateTimeField(auto_now_add=True)
    length = models.IntegerField(null=False)
    resources = models.FileField(upload_to='course_resources')
    price = models.IntegerField(null=False)
    discount_percentage = models.IntegerField(null=False, default=0)
    active_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

 
#implementing inheritance for Tag, Prerequisite and Learning models by creating parent class 'CourseProperty'
class CourseProperty(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=False)

    #don't want django to create table for this class 'CourseProperty' that's why
    class Meta:
        abstract = True

class Tag(CourseProperty):
    #course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    #description = models.CharField(max_length=50, null=False)
    pass

class Prerequisite(CourseProperty):
    #course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    #description = models.CharField(max_length=50, null=False)
    pass
    
class Learning(CourseProperty):
    #course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    #description = models.CharField(max_length=50, null=False)
    pass

class Video(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    serial_number = models.IntegerField(null=False)
    video_url = models.CharField(max_length=50, null=False)
    is_preview = models.BooleanField(default=False)