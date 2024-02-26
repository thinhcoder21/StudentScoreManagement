from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)

    def __str__(self):
        return self.username

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True,null=True)
    updated_date = models.DateField(auto_now=True,null=True)
    deleted_date = models.DateField(blank=True,null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Role(BaseModel):
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name

class Account(BaseModel):
    phone_number = models.CharField(max_length=255, unique=True, null=True)
    date_of_birth = models.DateField(null=True)
    account_status = models.BooleanField(default=False)
    gender = models.BooleanField(default=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=3)
    avatar = models.ImageField(upload_to='courses/%Y/%m', null=True, blank=True)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.user.username

class Course(BaseModel):
    name = models.CharField(max_length=255)

class Score(BaseModel):
    student = models.ForeignKey(Account,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    mid_term_score = models.FloatField(null=True, blank=True)
    final_term_score = models.FloatField(null=True, blank=True)

class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Các trường khác cho giáo viên

class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Các trường khác cho sinh viên

class Class(models.Model):
    name = models.CharField(max_length=255)
    account = models.ManyToManyField(Account,related_name='classes_enrolled',blank=True)

    def __str__(self):
        return self.name

class Post(BaseModel):
    post_content = RichTextField()
    comment_lock = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.post_content

class PostForum(BaseModel):
    post_forum_title =models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    post = models.OneToOneField(Post, on_delete= models.CASCADE)

    def __str__(self):
        return self.post_forum_title

class ForumQuestion(BaseModel):
    question_content = models.TextField()
    is_required = models.BooleanField(default=False)
    post_forum = models.ForeignKey(PostForum, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_content

class ForumReponse(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post_forum = models.ForeignKey(PostForum, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + ' - ' + self.post_forum.post_forum_title

class ForumAnswer(BaseModel):
    answer = models.CharField(max_length=255, null=True, blank=True)
    forum_question = models.ForeignKey(ForumQuestion , on_delete=models.CASCADE)
    forum_response = models.ForeignKey(ForumReponse, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer

