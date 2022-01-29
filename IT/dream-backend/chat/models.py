from django.db import models
from django.utils import timezone
from django.conf import settings
from users.models import CustomUser

# Create your models here.

class Message(models.Model):
    class MessageObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    timestamp = models.DateTimeField(default=timezone.now)
    body = models.CharField(max_length=250)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sender_Message')

    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='receiver_Message')
    objects = models.Manager()
    messageobjects = MessageObjects()


def __str__(self):
        return self.body



