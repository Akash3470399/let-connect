from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.fields import DateTimeField
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.user.username


class Message(models.Model):
    text = models.CharField(max_length=1000)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def getMessages(cls,logedInUser, friend):
        messages = Message.objects.all().filter(sender_id = logedInUser, receiver_id=friend) | Message.objects.all().filter(sender_id=friend, receiver_id = logedInUser)
        msgList = []
        for msg in messages:
            m = {
                'text':msg.text,
                'sender':msg.sender_id,
                'receiver':msg.receiver_id,
                'timestamp':msg.timestamp,
                }
            msgList.append(m)
        return msgList


class CustomUserManager(BaseUserManager):

    def create_user(self, email,name, password=None, **other_fields):
        if not email:
            raise ValueError(_("You must add email."))

        user = self.model(
             email = self.normalize_email(email),
             name = name,
             **other_fields,
         )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **other_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField(max_length=150, unique=False)
    friends = models.ManyToManyField('self', blank=True)
    start_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects = CustomUserManager()


    def __str__(self):
        return self.name
    

