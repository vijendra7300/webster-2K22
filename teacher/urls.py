from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views



urlpatterns = [
    path('',views.teacher_home_view,name='teacher_home'),
    path('profile/',views.teacher_profile,name='teacher_profile'),
    path('edit/',views.editProfile,name='editProfile'),
    
   path('notifybox/',views.notify_box,name='notify_box')
]