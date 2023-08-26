from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

import json


#import models of user profiles
from teacher.models import teacherProfile,Follower
from student.models import studentProfile

from .models import Room,Chats

from django.conf import settings 
from django.core.mail import send_mail
import os
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def chatindex(request):
    user=request.user
    if user.is_authenticated:
        return render(request,'chat/chat-index.html')    

    return redirect('login_page')


def create_room(request):
    user=request.user
    if user.is_authenticated:

        if request.method=='POST':
            user_obj = User.objects.get(username=user.email)
            password = request.POST.get('password')
            room_name = request.POST.get('roomName')
            limit  = request.POST.get('limit')
            which = request.POST.get('which')

            newroom = Room(admin=user_obj,roomName=room_name,limit=limit,password=password,which=which)
            Room.save(newroom)
            newroom.members.add(user_obj)
            newroom.save()
            return redirect('chatindex')

        return render(request,'chat/create-room.html')

    return redirect('login_page')



def join_room(request):
    user=request.user
    if user.is_authenticated:
        all_public_rooms = Room.objects.filter(which="public")
        print(all_public_rooms)
        return render(request,'chat/join-room.html',{'rooms':all_public_rooms})

    return redirect('login_page')



def handle_join_room(request):
    user=request.user
    if user.is_authenticated and request.method=='POST':
        room_name = request.POST.get('roomName')
        password = request.POST.get('password')

        currUser_obj = User.objects.get(username=user.email)    

        all_rooms = Room.objects.all()

        found = 0
        currRoom = None

        for room in all_rooms:
            if room.roomName==room_name:
                currRoom = room
                found = 1
                break

        if found:
            if currRoom.password==password:
                
                is_member = currRoom.members.filter(email=user.email)
               
                # Main chat html rendering............!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if not is_member:

                    blocked = currRoom.blocked.filter(email=user.email)
                    if blocked:
                        return HttpResponse("You have been banned from the room...!!")

                    if currRoom.members.count()==currRoom.limit:
                        return HttpResponse("<h1>Sorry the room is full</h1>")

                    else:
                        currRoom.members.add(currUser_obj)
                        currRoom.save()

                      
                room_chats = Chats.objects.filter(room=currRoom)
                is_admin = 1 if currRoom.admin.email==currUser_obj.email else 0
                all_members = []

                if is_admin:
                    all_members = list(currRoom.members.all())
                    #print(all_members)

                for i in all_members:
                    if i.email==currUser_obj.email:
                        all_members.remove(i)
                        break

                return render(request,'chat/chat-room.html',{'currRoom':currRoom , 'room_chats':room_chats ,
                                                            'currUser':currUser_obj.username , 'all_members':all_members , 'is_admin':is_admin})


            else:
                return HttpResponse("<h1>Wrong Password</h1>")


        else:
            return HttpResponse("<h1>No such room exists</h1>")

        return redirect('chatindex')

    elif user.is_authenticated:
        return redirect('chatindex')

    
    return redirect('login_page')




def get_chats(request,room_id):
    user=request.user
    if user.is_authenticated:
        room_obj = Room.objects.filter(id=room_id)

        if not room_obj:
            resp = {
            'check':"no room",
            'chats':"",
            'users':""
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")

        room_obj=room_obj[0]

        currUser_obj = User.objects.get(username = user.email)

        member = room_obj.members.filter(username = user.email)
        if member:
            room_chats = Chats.objects.filter(room=room_obj)
            chats=[]
            users = []

            for msg in room_chats:
                chats.append(msg.message)
                users.append(msg.by_whom.first_name)

            resp = {
                'check':"ok",
            'chats':chats,
            'users':users
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")


        else:
            resp = {
            'check':"not member",
            'chats':"",
            'users':""
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")

    return redirect('login_page')




def handlemsg(request,*args):
    user=request.user
    if user.is_authenticated:
        roomid = request.GET.get('roomid')
        room_obj = Room.objects.get(id=roomid)

        if not room_obj:
            resp = {
            'check':"room not there or u r not member of it",
            'msg':""
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")
        
        currUser_obj = User.objects.get(username = user.email)

        member = room_obj.members.filter(username = user.email) 

        if member:
            msg = request.GET.get('msg')
            newmsg = Chats(room=room_obj,by_whom=currUser_obj,message=msg)
            Chats.save(newmsg)

            resp = {
            'check':"ok",
            'msg':msg
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")


        else:
            resp = {
            'check':"room does not exist or u r not member of it",
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")

    return redirect('login_page')



def handleleave(request,*args):
    user=request.user
    if user.is_authenticated:
        print("yes")
        # username = request.session["username"]
        roomid = request.GET.get('roomid')
        room_obj = Room.objects.filter(id=roomid)

        if not room_obj:
            return redirect('chatindex')

        room_obj=room_obj[0]

        is_member = room_obj.members.filter(username=user.email)

        if is_member:
            is_admin = True if room_obj.admin.email == user.email else False

            if is_admin:
                room_obj.delete()
                all_chats=Chats.objects.filter(room=room_obj)
                all_chats.delete()

            else:
                room_obj.members.remove(is_member[0])
                all_chats = Chats.objects.filter(by_whom=is_member[0],room=room_obj)
                all_chats.delete()
                room_obj.save()

        
        return redirect('chatindex')

    return redirect('login_page')



def handlekick(request,*args):
    user=request.user
    if user.is_authenticated:
        roomid = request.GET.get('roomid')
        to_kick = request.GET.get('user')

        # curr_username = request.session["username"]
        curr_obj = User.objects.get(username=user.email)
        kick_obj = User.objects.get(username=to_kick)

        room_obj = Room.objects.get(id=roomid)


        if room_obj.admin.email==user.email:

            if to_kick==room_obj.admin.email:
                return redirect(request.META['HTTP_REFERER'])

            room_obj.members.remove(kick_obj)
            room_obj.save()

            resp = {
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")

        else:
            return redirect('chatindex')

    else:
        return redirect('login_page')


        
def handleban(request):
    user=request.user
    if user.is_authenticated:
        roomid = request.GET.get('roomid')
        to_ban = request.GET.get('user')

        # curr_username = request.session["username"]
        curr_obj = User.objects.get(username=user.email)
        ban_obj = User.objects.get(username=to_ban)

        room_obj = Room.objects.get(id=roomid)


        if room_obj.admin.email==user.email:

            if to_ban==room_obj.admin.email:
                return redirect(request.META['HTTP_REFERER'])

            room_obj.members.remove(ban_obj)
            room_obj.blocked.add(ban_obj)
            room_obj.save()

            resp = {
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")

        else:
            return redirect('chatindex')

    else:
        return redirect('login_page')



