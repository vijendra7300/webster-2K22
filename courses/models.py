from django.db import models
from teacher.models import teacherProfile
from student.models import studentProfile

from django.contrib.auth import get_user_model


User=get_user_model()


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50,default="")
    teacher = models.ForeignKey(teacherProfile,on_delete = models.CASCADE)
    num_vid = models.IntegerField(default=0)
    description = models.CharField(max_length=50,default="",blank=True)
    thumbnail = models.ImageField(upload_to = "course_thumbnails",default="course_thumbnails/def_cour_thumb.jpeg")

    def __str__(self):
       return self.name


class subscription(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    student = models.ForeignKey(studentProfile, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.course)


class Video(models.Model):
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    likes = models.ManyToManyField(studentProfile,related_name='likes_post',blank=True)
    views = models.ManyToManyField(User,related_name='tot_views',blank=True)
    date = models.DateTimeField(auto_now_add=True)
    dislikes = models.ManyToManyField(studentProfile,related_name='dislikes_post',blank=True)
    title = models.CharField(max_length=50,default="")
    description = models.CharField(max_length=500,default="")
    video = models.FileField(upload_to = "course_videos",blank=True)
    vid_thumbnail = models.ImageField(upload_to="vid_thumbs",blank=True)

    @classmethod
    def liked_p(cls, user, id):
        vid = cls.objects.get(pk=id)
        print("liked")
        vid.likes.add(user)

    @classmethod
    def disliked_p(cls, user, id):
        vid = cls.objects.get(pk=id)
        print("disliked")
        vid.dislikes.add(user)

    @classmethod
    def rem_liked_p(cls, user, id):
        vid = cls.objects.get(pk=id)
        print("removed liked")
        vid.likes.remove(user)

    @classmethod
    def rem_disliked_p(cls, user, id):
        vid = cls.objects.get(pk=id)
        print("remove disliked")
        vid.dislikes.remove(user)

    @classmethod
    def add_view(cls,user,id):
        vid = cls.objects.get(pk=id)
        vid.views.add(user)

    class Meta:
        ordering=['-date']

    
    def __str__(self):
       return str(self.course_id.id) + " "+self.title

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    msg = models.CharField(max_length=50,blank=True,default="")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-time']

    def str(self):
        return str(self.msg)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    msg = models.CharField(max_length=50,blank=True,default="")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-time']

        def __str__(self):
            return str(self.msg)




        
