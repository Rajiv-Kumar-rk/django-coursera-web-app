from django.shortcuts import render, HttpResponse, redirect
from App_Course.models import Course, Tag, Prerequisite, Learning, Video
from App_CourseTransaction.models import UserCourse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    courses = Course.objects.all()
    
    data = {
        'courses' : courses
    }
    return render(request, 'App_Course/index.html', context=data)

def course_page(request, slug):
    course = Course.objects.get(slug=slug)
    course_lecture_list = Video.objects.filter(course = course).order_by('serial_number')

    curr_lec_serial_number = request.GET.get('lecture')

    if curr_lec_serial_number is None:
        curr_lec_serial_number = 1
    
    prev_lecture = None
    next_lecture = None

    #set next_lecture serial number
    next_lecture = int(curr_lec_serial_number)+1
    if next_lecture > len(course_lecture_list): #if 
        next_lecture = None
    
    #set prev_lecture serial number
    prev_lecture = int(curr_lec_serial_number)-1
    if curr_lec_serial_number == 1:
        prev_lecture = None


        
    video_lec =  Video.objects.get(course=course, serial_number = curr_lec_serial_number)

    if video_lec.is_preview is False:
        if request.user.is_authenticated is False:
            return redirect('enroll_to_course', slug=course.slug)
        else:
            try: #is the user is enroll to this course?
                user_course_obj = UserCourse.objects.get(user=request.user, course = course)
            except:
                return redirect('enroll_to_course', slug=course.slug)
        
    data = {
        'course' : course,
        'current_video_lecture' : video_lec,
        'course_lecture_list' : course_lecture_list,
        'previous_lecture' : prev_lecture,
        'next_lecture' : next_lecture
    }
    return render(request, 'App_Course/course_page.html', context=data)

@login_required(login_url='user_login')
def my_courses(request):
    user_courses = UserCourse.objects.filter(user = request.user)
        
    data = {
        'user_courses' : user_courses
    }
    return render(request, 'App_Course/myCourses.html', context=data)
 