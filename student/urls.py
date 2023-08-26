from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views



urlpatterns = [
    path('',views.student_home_view,name='student_home'),
    path('profile/',views.student_profile,name='student_profile'),
    path('edit/',views.edit,name='edit'),
    path('searched_teacher_profile/<int:teacher_id>/',views.searched_teacher_view,name='searched_teacher'),
    path('follow/',views.handlefollow,name='follow'),
    path('result/',views.student_result,name='student_result'),
    path('manage_edit/',views.manage_edit,name='manage_edit'),
    path('see_courses/<int:teacherId>',views.see_course, name='see_courses'),
    path('hmm/',views.hue,name='huehue')
    
]