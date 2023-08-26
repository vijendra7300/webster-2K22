from django.db import models
from student.models import studentProfile
# Create your models here.


class teacherProfile(models.Model):
    teacher_id=models.AutoField
    firstname=models.CharField(max_length=100,default="",blank=True)
    lastname=models.CharField(max_length=100,default="",blank=True)
    # mobile=models.IntegerField(default=0)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=25)
    address = models.CharField(max_length=100,default="",blank=True)
    profileImage = models.ImageField(upload_to = "teacherImages",default="teacherImages/def_user.png",blank=True)
    country = models.CharField(max_length=25,default="",blank=True)
    state = models.CharField(max_length=25,default="",blank=True)
    tagline = models.CharField(max_length=100,default="Keep Learning")

    
    def __str__(self):
       return self.firstname+" "+self.lastname + str(self.id)


class Follower(models.Model):
    teacher = models.OneToOneField(teacherProfile, on_delete=models.CASCADE)
    students = models.ManyToManyField(studentProfile,related_name="follower")
    
    @classmethod
    def follow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(teacher=currUser)
        obj.students.add(to_follow)
        

    @classmethod
    def unfollow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(teacher=currUser)
        obj.students.remove(to_follow)

    def __str__(self):
       return self.teacher.firstname




class Following(models.Model):
    student = models.OneToOneField(studentProfile, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(teacherProfile,related_name="followed")
    
    @classmethod
    def follow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(student=currUser)
        obj.teachers.add(to_follow)
        

    @classmethod
    def unfollow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(student=currUser)
        obj.teachers.remove(to_follow)

    def __str__(self):
       return self.student.firstname




