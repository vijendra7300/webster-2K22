from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth import get_user_model


User=get_user_model()

class forgotPassword(models.Model):
    email = models.EmailField(max_length=100)
    token = models.CharField(max_length=500)
    datastamp = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    user =  models.ForeignKey(User , on_delete=models.CASCADE)
    message = models.TextField(max_length=30,default="")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-time']


