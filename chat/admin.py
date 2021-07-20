from django.contrib import admin
from .models import Message, Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)