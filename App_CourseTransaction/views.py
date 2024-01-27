from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from App_Course.models import Course, Tag, Prerequisite, Learning, Video
from App_CourseTransaction.models import UserCourse, Payment
from django.views.decorators.csrf import csrf_exempt #to handle post request made by razorpay verify page
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail #library for sending mail to target user

#creating client to razorpay
from skillGliding.settings import *
from time import time

import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


# Create your views here.
@login_required(login_url='user_login')
def checkout_course(request, slug):
    course = Course.objects.get(slug=slug)

    '''
    if not request.user.is_authenticated:
        return redirect('user_login')
    '''

    action = request.GET.get('action')
    user = request.user
    #creating order object to proceed to payment task
    #razorpay will give order id when server give the order object razorpay api 
    order = None
    error = None

    #to restrict the re-payment for the same course
    try:
        user_course_obj = UserCourse.objects.get(user = user, course = course)
        #if object is present, then show error(to restrict the re-payment for the same course)
        error = "You are already enrolled to this course!"
    except:
        pass

    amount = None

    if error is None: #no object is present
        amount = int((course.price - (course.price * course.discount_percentage*0.01)) *100) #convert into rupee into paise(int)

    if amount==0:#enroll the user to the course for free with creating order and payment object for the user
        user_course_obj = UserCourse(user = user, course = course)
        user_course_obj.save()

        #sending mail on course enrollemnt confirmation to the user
        mail_message_body = 'Thank you for purchasing our course! We are pleased to confirm your enrollment to the course({}). We hope you find it valuable and enjoyable. Good Luck for your learning journey!'.format(course.name)
        mail_receiver_address = request.user.email
        send_mail(
            'Course Enrollment Confirmation Status', #subject of mail here
            mail_message_body, #content or body of mail here
            'skillgliding@gmail.com', #sender's mail address here
            [mail_receiver_address], #receiver's mail address here
            fail_silently=False
        )

        return redirect('course', slug=course.slug)

    if action == 'create_payment': #else if, amount is above to 0, then create order and payment object for the user
        currency = "INR"
        notes = {
            'name' : user.first_name + " " + user.last_name,
            'email' : user.email,
            'course_name' : course.name,
            'course_price' : "Rs. "+str(int((course.price - (course.price * course.discount_percentage*0.01)) *100))
        }
        receipt_id = "SkillGliding-"+str(int(time()))
        order = client.order.create(
            {
                "receipt" : receipt_id, 
                "amount" : amount, 
                "currency" : currency, 
                "notes" : notes
            }
        )

        #now, after collecting order id from razorpay api
        #create payment object for the above created order object
        payment = Payment()
        payment.user = user
        payment.course = course
        payment.order_id = order.get('id')
        payment.save() #save the object to database

    data = {
        'course' : course,
        'order' : order,
        'error' : error
    }
    return render(request, 'App_CourseTransaction/checkout_page.html', context=data)

@csrf_exempt 
def verify_payment(request): #url to match this function is created in main App urls.py file
    
    if request.method == 'POST':
        data_received = request.POST #will give razorpay_payment_id, razorpay_order_id, razorpay_signature 

        try:
            #print(data_received)
            client.utility.verify_payment_signature(data_received)
            #if (generated_signature == razorpay_signature) so,  payment is successful, then
            razorpay_order_id = data_received.get('razorpay_order_id')
            razorpay_payment_id = data_received.get('razorpay_payment_id')
            
            #update the payment object in the database on getting successful payment 
            payment_obj = Payment.objects.get(order_id = razorpay_order_id)
            
            payment_obj.payment_id = razorpay_payment_id
            payment_obj.payment_status = True 

            userCourse_obj = UserCourse()
            userCourse_obj.user = payment_obj.user
            userCourse_obj.course = payment_obj.course
            userCourse_obj.save()

            payment_obj.user_course = userCourse_obj
            payment_obj.save()

            #sending mail on course enrollemnt confirmation to the user
            mail_message_body = 'Thank you for purchasing our course! We are pleased to confirm your enrollment to the course({}). We hope you find it valuable and enjoyable. Good Luck for your learning journey!'.format(userCourse_obj.course.name)
            mail_receiver_address = request.user.email
            send_mail(
                'Course Enrollment Confirmation Status', #subject of mail here
                mail_message_body, #content or body of mail here
                'skillgliding@gmail.com', #sender's mail address here
                [mail_receiver_address], #receiver's mail address here
                fail_silently=False
            )

            user_courses = UserCourse.objects.filter(user = request.user)
            #print(razorpay_order_id, razorpay_payment_id, payment_obj, userCourse_obj)
            data = {
                'user_courses' : user_courses
            }
            return render(request, 'App_Course/myCourses.html', context=data)

        except:
            return HttpResponse("Invalid Payment Details")
