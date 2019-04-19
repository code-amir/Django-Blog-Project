from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    GENDER = (
    ('m', 'Male'),
    ('f', 'Female'),
    )
    gender = models.CharField(
    max_length=1,
        choices=GENDER,
        default='m',
    )
    pincode = models.IntegerField(validators=[MinValueValidator(100000),MaxValueValidator(999999)])
    email_id = models.EmailField(primary_key=True)
    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('UserProfileInfo',on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post',on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("blog:post_list")

    def __str__(self):
        return self.text
