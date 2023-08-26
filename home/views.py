from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4
#import models of user profiles
from teacher.models import teacherProfile,Follower
from student.models import studentProfile
from .models import forgotPassword
from .models import Notification

from django.conf import settings 
from django.core.mail import send_mail
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
# import string,random


# s1=string.ascii_lowercase
# s2=string.digits
# s3=string.ascii_uppercase
# s=[]
# s.extend(list(s1))
# s.extend(list(s2))
# s.extend(list(s3))


# def otp_generator():
#     random.shuffle(s)
#     return str("".join(s[0:6]))



def home_view(request):
    user=request.user
    if user.is_authenticated:
        return redirect('login_page')
    return render(request,'home/index.html',{})


def login_user(request):

    user=request.user
    if user.is_authenticated:
        if "category" in request.session:
            catg = request.session["category"]
            print(catg)
            if catg=="student":
                print("hello student")
                return redirect('student_home')
        return redirect('teacher_home')

    if request.method == 'POST':
        femail = request.POST.get('email',"")
        fpassword = request.POST.get('password',"")
        
        all_users = User.objects.all()

        conf_user = authenticate(username=femail,password=fpassword)

        if conf_user:
            login(request,conf_user)

            is_teacher = teacherProfile.objects.filter(email=femail)
            if len(is_teacher)==0:
                is_teacher=0
            else:
                is_teacher=1

            if is_teacher:
                request.session["category"]="teacher"
                return redirect('teacher_home')

            else :
                request.session["category"]="student"
                return redirect('student_home')

        messages.error(request,"Invalid Credentials")
        return redirect(request.path)

    return render(request, 'home/login.html')



def signup_user(request):

    user=request.user
    if user.is_authenticated:
        return redirect('teacher_home')

    if request.method=='POST':
        fname = request.POST.get('firstname',"")
        lname=request.POST.get('lastname',"")
        femail = request.POST.get('emailid',"")
        passw = request.POST.get('password',"")
        confpass = request.POST.get('confirmpassword',"")
        categ = int(request.POST.get('category',""))

        print(categ)
        
        #password didn't match
        if passw!=confpass:
            messages.error(request, "Password did not match.")
            return redirect(request.path)

        #already taken email
        all_users=User.objects.all()

        for user in all_users:
            if user.email==femail:
                messages.error(request, "Email Already taken")
                return redirect(request.path)
        
        curr_user=User.objects.create_user(femail,femail,passw)
        curr_user.first_name=fname
        curr_user.last_name=lname
        curr_user.save()

        if categ==1:
            print("1")
            newTeacher = teacherProfile(firstname=fname,lastname=lname,email=femail,password=passw)
            teacherProfile.save(newTeacher)
        else:
            print("2")
            newStudent = studentProfile(firstname=fname,lastname=lname,email=femail,password=passw)
            studentProfile.save(newStudent)

        user=authenticate(username=femail,password=passw)
        if user:
            login(request,user)
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [femail]
            # send_mail(subject,message,email_from,recipient_list)

            # login(request, femail)
            # request.session
            # messages.success(request, "Sign Up successful! Verify Your Email to Continue!")
            if categ==1:
                return redirect('teacher_home')
            return redirect('student_home')
            
    return render(request, 'home/signup.html')



def logout_user(request):
    logout(request)
    if "category" in request.session:
        del request.session["category"]
    return redirect('home_view')
    

def validate_user(request):
    if(request.user.is_authenticated):
        print("user is authenticated")
        try:
            teacher = teacherProfile.objects.get(email=request.user.email)
        except teacherProfile.DoesNotExist:
            teacher = None

        try:
            student = studentProfile.objects.get(email=request.user.email)
        except studentProfile.DoesNotExist:
            student = None

        

        if teacher is not None:
            print('user is a teacher')
            return redirect('teacher_home') #for real purpose redirect to teacher dashboard
        if student is not None:
            print('user is a student')
            print(student.email)
            return redirect('student_home') #for real purpose redirect to student dashboard

        user=request.user
        user.username=user.email
        user.save()

        print("User has not selected its occupation")
        return render(request,'home/occupation.html')
    print("user is not authenticated")
    return redirect('home_view')


    
def student_confirm(request):
    if(request.user.is_authenticated):
        print("user is authenticated")
        try:
            teacher = teacherProfile.objects.get(email=request.user.email)
        except teacherProfile.DoesNotExist:
            teacher = None
        try:
            student = studentProfile.objects.get(email=request.user.email)
        except studentProfile.DoesNotExist:
            student = None
        if teacher is not None:
            print('user is a teacher')
            return redirect('teacher_home') #for real purpose redirect to teacher dashboard
        if student is not None:
            print('user is a student')
            return redirect('student_home') #for real purpose redirect to student dashboard
        newStudent = studentProfile(email=request.user.email)
        studentProfile.save(newStudent)
        return redirect('student_home') #for real purpose redirect to student dashboard        
    print("user is not authenticated")
    return redirect('home_view')



def teacher_confirm(request):
    if(request.user.is_authenticated):
        print("user is authenticated")
        try:
            teacher = teacherProfile.objects.get(email=request.user.email)
        except teacherProfile.DoesNotExist:
            teacher = None
        
        if teacher is not None:
            print('user is a teacher')
            return redirect('teacher_home') #for real purpose redirect to teacher dashboard
        
        newTeacher = teacherProfile(email=request.user.email)
        teacherProfile.save(newTeacher)
        
        return redirect('home_view') #for real purpose redirect to student dashboard   
             
    print("user is not authenticated")
    return redirect('home_view')

def handle_forgot_password(request):
    if request.method == "POST":
        email_user = request.POST.get('email')
        # email = forgotPassword.objects.filter(email=email_user)
        # if email is not None:
        
        student = studentProfile.objects.filter(email=email_user)
        teacher = teacherProfile.objects.filter(email=email_user)
        if len(teacher)!=0 and len(student)!=0:
            return redirect('validate_user')
        token = uuid4()

        content = f"http://127.0.0.1:8000/auth_forgot/{token}"
        print(content)
        send_mail('Forgot_password',content,'techstartechtechstar@gmail.com',[email_user],fail_silently=False)
        new_forgot = forgotPassword(email=email_user,token=token)
        new_forgot.save()
        return redirect('success_forgot_password')
       
    return redirect('home_view')
def auth_forgot_password(request,token):
    forgotpassword = forgotPassword.objects.filter(token=token)
    if len(forgotpassword)!=0:
        print(forgotpassword[0].email)
        response = {
                    'token':token,
                    }
        return render(request,'home/resetpassword.html',response)
    return redirect('home_view')
        

        
def reset_password(request,token):
    if request.method == "POST":
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        # if (new_password != confirm_password):
        #     response = {
        #             'token':token,
        #             }
        #     return render(request,'home/resetpassword.html',response)
        forgotpassword = forgotPassword.objects.filter(token=token)
        if len(forgotpassword):
            email = forgotpassword[0].email
            forgotpassword.delete()
            student = studentProfile.objects.filter(email=email)
            teacher = teacherProfile.objects.filter(email=email)
            print(len(student),len(teacher))
            if len(student):
                student[0].password = new_password
                print("student password is changed")
            if len(teacher):
                teacher[0].password = new_password
                print("teacher password is changed")
    return redirect('home_view')



def notify(request):
    user=request.user
    if user.is_authenticated:
        all_notify_obj = Notification.objects.filter(user=user)
        all_msg=[]
        for i in all_notify_obj:
            all_msg.append(i)
        return render(request,'home/notification.html',{'notify':all_msg})
    return redirect('login_page')


def delete_notify(request,notify_id):
    user=request.user
    if user.is_authenticated:
        curr_notify = Notification.objects.filter(id=notify_id)

        if len(curr_notify)!=0:
            curr_notify.delete()
            
        return redirect('notification')


    return redirect('login_page')


def deleteAll(request):
    user=request.user
    if user.is_authenticated:
        curr_notify_obj = Notification.objects.filter(user=user)
        if curr_notify_obj:
            for i in curr_notify_obj:
                i.delete()

        return redirect('notification')

    return redirect('login_page')
