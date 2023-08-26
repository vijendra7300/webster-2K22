from django.contrib import admin

# Register your models here.
from .models import teacherProfile,Follower,Following

admin.site.register(teacherProfile)
admin.site.register(Follower)
admin.site.register(Following)
