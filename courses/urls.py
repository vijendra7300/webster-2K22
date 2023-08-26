from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('add_courseform/',views.course_form,name='course_form'),
    path('<int:teacher_id>/',views.teacher_courses,name='teacher_course'),
    path('handle_comment/',views.handle_comment,name='handle_comment'),
    path('student/<int:student_id>/',views.student_courses,name='student_course'),
    
    path('seecourse/<int:course_id>/',views.seecourse,name='see_course'),
    path('see_video/<int:video_id>/',views.see_video,name='see_video'),
    path('add_video/<int:course_id>/',views.addvideo,name='add_video'),
    path('next_video/',views.nextvideo_view,name='nextvideo'),
    path('delete/<int:courseId>/',views.deleteCourse,name="delete"),
    path('delete_video/<int:videoId>/',views.deleteVideo,name="delete_video"),
    path('like_video/',views.handle_like,name='like_func'),

    path('subscribeCourse/',views.handle_subscribe,name='subscribe_course'),
    
]