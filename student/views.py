from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import studentProfile
from  teacher.models import teacherProfile,Follower,Following

from courses.models import Course,Video
import json
import requests



def student_home_view(request):
    print("hello student")
    user = request.user
    if user.is_authenticated:
        print(user.email)
        curr_user=studentProfile.objects.get(email=user.email)
        # print(curr_user.id)

        all_following_obj = Following.objects.filter(student=curr_user)
        
        users_following=[]

        if all_following_obj:
            users_following = all_following_obj[0].teachers.all()

        all_courses=Course.objects.all()
        feed_vids=[]

        for i in all_courses:
            if i.teacher in users_following:
                courseid=i.id
                videos_obj = Video.objects.filter(course_id=courseid)

                for j in videos_obj:
                    feed_vids.append(j)

        for i in feed_vids:
            print(i)

        return render(request, 'student/dashboard.html',{'user':curr_user,'feed_vids':feed_vids})

    messages.error(request,"Login First")
    return redirect('login_page')


def isUserMatching(str1 , str2):
    #Filters user based on search
    m = len(str1) 
    n = len(str2) 
      
    j = 0   
    i = 0   
      
    while j<m and i<n: 
        if str1[j] == str2[i]:     
            j = j+1    
        i = i + 1
          
    # If all characters of str1 matched, then j is equal to m 
    return j==m



def student_result(request):
    print("hello")
    user = request.user
    if user.is_authenticated:
        curr_user=studentProfile.objects.get(email=user.email)
        # print(curr_user.id)
        name = request.POST.get('search')
        print(name)
        teachers = teacherProfile.objects.all()
        mylist = []
        for i in teachers:
            if isUserMatching(i.firstname,name) or isUserMatching(i.lastname,name) or isUserMatching(name, i.lastname) or isUserMatching(name, i.firstname):
                            mylist.append(i)           
        return render(request, 'student/result.html',{'teachers':mylist})

    messages.error(request,"Login First")
    return redirect('login_page')


def student_profile(request):
    user = request.user
    if user.is_authenticated:
        curr_user = studentProfile.objects.get(email=user.email)
        user_tags = curr_user.tagline
        profileImage = curr_user.profileImage

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

        return render(request, 'student/profile.html', {'user':curr_user,'word_list':tag_list , 'profileImage':profileImage})

    messages.error(request,"Login First")
    return redirect('login_page')




def searched_teacher_view(request,teacher_id):
    user=request.user
    if user.is_authenticated:
        curr_teacher=teacherProfile.objects.filter(id=teacher_id)
        if not curr_teacher:
            return redirect('login_page')

        curr_teacher=curr_teacher[0]
        curr_student = studentProfile.objects.get(email=user.email)
        follower = Follower.objects.filter(teacher=curr_teacher,students=curr_student)   

        tot_f = Follower.objects.filter(teacher=curr_teacher)

        all_f =tot_f[0].students.count()   

        if  not follower:
            follower=0
        else:
            follower=1

        return render(request, 'student/searchedteacher.html',{'id':teacher_id,'all_f':all_f,'curr_teacher':curr_teacher,'follower':follower})

    return redirect('login_page')



def handlefollow(request,*args):
    
    user=request.user
    if user.is_authenticated:
        teacher_id=request.GET.get('teacher_id')
        print(teacher_id)
        curr_teacher = teacherProfile.objects.filter(id=teacher_id)

        if len(curr_teacher)==0:
            return redirect('login_page')

        curr_teacher=curr_teacher[0]
        curr_user = studentProfile.objects.get(email=user.email)

        is_followed = Following.objects.filter(student=curr_user,teachers=curr_teacher)

        if is_followed:
            print("unfollow")
            Following.unfollow(curr_user, curr_teacher)
            Follower.unfollow(curr_teacher, curr_user)
        else:
            print("follow")
            Follower.follow(curr_teacher, curr_user)
            Following.follow(curr_user, curr_teacher)
        print("heelo")
        tot=Follower.objects.filter(teacher=curr_teacher)
        tot=tot[0].students.count()
        rep={
            'tot':tot
        }
        print(tot)
        response=json.dumps(rep)

        return HttpResponse(response,content_type='application/json')

    return redirect('login_page')

def edit(request):
    user = request.user
    if user.is_authenticated:
        curr_student = studentProfile.objects.get(email=user.email)
        fname = curr_student.firstname
        lname = curr_student.lastname
        address = curr_student.address
        state = curr_student.state
        country = curr_student.country
        password = curr_student.password
        email = curr_student.email
        profileImage = curr_student.profileImage
        return render(request , 'student/editprofile.html' , {'fname':fname , 'lname':lname , 'address':address , 'state':state,
                                                            'country':country , 'password':password, 'email':email, 'profileImage':profileImage    })



def manage_edit(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            fname = request.POST.get('firstname',"")
            lname = request.POST.get('lastname',"")
            passw = request.POST.get('password',"")
            st = request.POST.get('state',"")
            coun = request.POST.get('country',"")
            profPic = request.FILES.get('profilePic',"")
            addr = request.POST.get('address',"")

            curr_user = studentProfile.objects.get(email=user.email)
            ori_password=curr_user.password

            curr_user.firstname=fname
            curr_user.lastname=lname
            curr_user.password=passw
            curr_user.state=st
            curr_user.country=coun
            curr_user.address=addr

            if len(profPic):
                curr_user.profileImage=profPic
                # print(profPic + "kklksldksds")

            curr_user.save()

            if ori_password==passw:
                return redirect('login_page')

            user.first_name=fname
            user.last_name=lname
            user.set_password(passw)
            user.save()
        
            user=authenticate(username=user.email,password=passw)
            login(request,user)
            request.session["category"]="student"
            return redirect('login_page')

    messages.error(request,"Login in First")
    return redirect('login_page')




    return render(request , 'student/editprofile.html')

def hue(request):
    rep={'name':890}
    response=json.dumps(rep)
    return requests.post('http://127.0.0.1:3000/', params = response)

def see_course(request , teacherId):
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect(reverse('teacher_course',kwargs={'teacher_id':teacherId}) )
