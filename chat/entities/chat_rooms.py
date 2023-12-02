from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active_client      = models.IntegerField()
    max_client      = models.IntegerField()


    def __str__(self):
        return self.name
