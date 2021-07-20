from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')

    def __str__(self):
        return self.user.username

    def getMessages(self, friend):
        messages = Message.objects.all().filter(sender_id = self.user.id, receiver_id=friend) | Message.objects.all().filter(sender_id=friend, receiver_id = self.user.id)
        msgDict = []
        for msg in messages:
            m = {
                'text':msg.text,
                'sender':msg.sender_id,
                'receiver':msg.receiver_id,
                'timestamp':msg.timestamp,
                }
            msgDict.append(m)
        return msgDict

class Message(models.Model):
    text = models.CharField(max_length=1000)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
