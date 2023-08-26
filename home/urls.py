from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('',views.home_view,name='home_view'),
    path('login/',views.login_user,name='login_page'),
    path('signup/',views.signup_user,name='signup_page'),
    path('logout/',views.logout_user,name='logout'),
    path('forgot/',TemplateView.as_view(template_name='home/forgotpassword.html')),   #redirect here to  initiate forgotpassword
    path('forgotpassword/',views.handle_forgot_password,name='handle_forgot_password'), #After user submits forgotpassword.html
    path('successforgotpassword/',TemplateView.as_view(template_name='home/successforgotpassword.html'),name='success_forgot_password'), #succefully sent the forgot mail
    path('auth_forgot/<str:token>',views.auth_forgot_password,name="auth_forgot_password"),
    path('resetpassword/<str:token>',views.reset_password,name="reset_password"),
    path('user/google/validate/',views.validate_user,name='validate_user'), #Use This to redirect any user to its right place
    path('user/student/confirm/',views.student_confirm,name='student_confirm'),#Setting new Students here
    path('user/teacher/confirm/',views.teacher_confirm,name='teacher_confirm'), #Setting new Teacher here

    path('notification/',views.notify,name='notification'),
    path('delete_notify/<int:notify_id>/',views.delete_notify,name='delete_notify'),
    path('deleteAll/',views.deleteAll,name='deleteAll')
]
