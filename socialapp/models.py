from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from autoslug import AutoSlugField
from django.utils.text import slugify

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, full_name,gender,profile_pic, date_of_birth, password=None,conf_password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            full_name = full_name,
            gender = gender,
            date_of_birth=date_of_birth,
            profile_pic = profile_pic
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,full_name,gender, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            full_name = full_name,
            gender = gender,
            password=password,
            
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('male','male'),
        ('female','female'),
        ('others','others'),
    )
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name","gender","date_of_birth"]


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class ProfilePicture(models.Model):
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = (
        ('current','current'),
        ('changed','changed')
    )
    status = models.CharField(max_length=100, choices=status_choices, default="current")
    
    def __str__(self) -> str:
        return f'{self.user.full_name} - {self.profile_pic}'
    

class Post(models.Model):
    post_content = models.TextField()
    post_image = models.FileField(upload_to="post_images/", null=True, blank=True)
    likes = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'{self.post_content} - by {self.user.full_name}'

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    user = models.ForeignKey(User, models.CASCADE, related_name="liked_by")
    
    def __str__(self):
        return f'{self.post} liked by {self.user.full_name} '
    
   



class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to")
    
    friends_choices = (
        ('unchecked','unchecked'),
        ('accepted','accepted'),
        ('rejected','rejected')
    )
    status = models.CharField(max_length=100, choices=friends_choices, default="unchecked")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(null=True, blank=True)
    slug = models.SlugField(editable=False, blank=True, null=True)
    class Meta:
        ordering = ('-created',)
    
    
    def save(self, *args, **kwargs):
        if self.id:
            slug_field = f'{self.sender.full_name} {self.sender.id} {self.to.full_name} {self.to.id}'
            self.slug = slugify(slug_field)

        super(FriendRequest, self).save()
    
    def __str__(self) -> str:
        return f'send by {self.sender.full_name} to {self.to.full_name}'


class UserChat(models.Model):
    message = models.CharField(max_length=100)
    msg_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_from")
    msg_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_to")
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    friends_rel = models.ForeignKey(FriendRequest, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.msg_from.full_name} - to - {self.msg_to}'