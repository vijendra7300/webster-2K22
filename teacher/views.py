from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import teacherProfile

from .models import Follower

from home.models import Notification


def teacher_home_view(request):
    user = request.user
    if user.is_authenticated:
        curr_user=teacherProfile.objects.get(email=user.email)
        # print(curr_user.id)
        return render(request, 'teacher/dashboard.html',{'user':curr_user})

    messages.error(request,"Login First")
    return redirect('login_page')



def teacher_profile(request):
    user = request.user
    if user.is_authenticated:
        curr_user = teacherProfile.objects.get(email=user.email)
        user_tags = curr_user.tagline

        tag_list=[]
        currword=""
        spcount=0
        for ch in user_tags:
            if ch==' ':
                spcount+=1
        
            if spcount>4:
                tag_list.append(currword)
                spcount=0
                currword=""
            else:
                currword+=ch
        currword+='  "'
        tag_list.append(currword)

        return render(request, 'teacher/teacher_profile.html', {'user':curr_user,'word_list':tag_list})

    messages.error(request,"Login First")
    return redirect('login_page')



def editProfile(request):
    user=request.user
    if user.is_authenticated:
        # print("hello")
        if request.method=='POST':
            fname = request.POST.get('firstname',"")
            lname = request.POST.get('lastname',"")
            passw = request.POST.get('password',"")
            st = request.POST.get('state',"")
            coun = request.POST.get('country',"")
            profPic = request.FILES.get('profilePic',"")
            addr = request.POST.get('address',"")
            tagl  = request.POST.get('tagline',"")

            # if len(passw)==0:
            #     passw=otp_generator()
            # print(passw)
            curr_user = teacherProfile.objects.get(email=user.email)
            ori_password=curr_user.password

            curr_user.firstname=fname
            curr_user.lastname=lname
            curr_user.password=passw
            curr_user.state=st
            curr_user.country=coun
            curr_user.address=addr
            curr_user.tagline=tagl
            

            if len(profPic):
                curr_user.profileImage=profPic
            curr_user.save()

            if ori_password==passw:
                return redirect('login_page')

            user.first_name=fname
            user.last_name=lname
            user.set_password(passw)
            user.save()

        # messages.success(request, {'msg':"Details updated successfully" , })
        
            user=authenticate(username=user.email,password=passw)
            login(request,user)
            request.session["category"]="teacher"
            return redirect('login_page')

    messages.error(request,"Login in First")
    return redirect('login_page')



def notify_box(request):
    user=request.user
    if user.is_authenticated:
        if request.method=='POST':

            catg=1
            if "category" in request.session:
                catg=request.session["category"]
            if catg=="student":
                return redirect('login_page')

            msg=request.POST.get('msg',"")

            curr_teacher=teacherProfile.objects.get(email=user.email)
            curr_follower_obj=Follower.objects.filter(teacher=curr_teacher)


            if len(curr_follower_obj)!=0:
                curr_follower_obj=curr_follower_obj[0]
                all_fllw = curr_follower_obj.students.all()
                # print(all_fllw)
                for i in all_fllw:
                    auth_i=User.objects.get(username=i.email)
                    mssg = str(curr_teacher.firstname)+" "+str(curr_teacher.lastname)+" : "+msg
                    newNotify = Notification(user=auth_i,message=mssg)
                    newNotify.save()
            
            return redirect('login_page')


        return render(request,'teacher/box.html')

    return redirect('login_page')
