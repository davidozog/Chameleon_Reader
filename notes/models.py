from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    user = models.ForeignKey(User)
    title   = models.CharField(max_length=255)
    content = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True) 
    last_update = models.DateTimeField(auto_now=True)
