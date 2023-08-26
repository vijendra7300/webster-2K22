from django.db import models

# Create your models here.


class studentProfile(models.Model):
    student_id=models.AutoField
    firstname=models.CharField(max_length=100,default="",blank=True)
    lastname=models.CharField(max_length=100,default="",blank=True)
    # mobile=models.IntegerField(default=0)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=25)
    address = models.CharField(max_length=100,default="",blank=True)
    profileImage = models.ImageField(upload_to = "studentImages",default="teacherImages/def_user.png",blank=True)
    country = models.CharField(max_length=25,default="",blank=True)
    state = models.CharField(max_length=25,default="",blank=True)
    tagline = models.CharField(max_length=100,default="Keep Learning")

    def __str__(self):
        return self.firstname+" "+self.lastname



