from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('teacher/',include('teacher.urls')),
    path('courses/',include('courses.urls')),
    path('student/',include('student.urls')),
    path('chat/',include('chat.urls')),
    path('paytm/',include('paytm.urls'))
] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)