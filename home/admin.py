from django.contrib import admin

# Register your models here.
from .models import forgotPassword



from .models import Notification

admin.site.register(Notification)
admin.site.register(forgotPassword)