from django.db import models
from django.contrib.auth.models import User
from contents.models import Achievement
     
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    age = models.IntegerField()
    achievements = models.ManyToManyField(Achievement)
    language = models.CharField(max_length=50)
    steamid = models.CharField(max_length=50)
    avatar_large = models.FileField(blank=True, null=True, upload_to="static/img/avatars")
    avatar_medium = models.FileField(blank=True, null=True, upload_to="static/img/avatars")
    avatar_small = models.FileField(blank=True, null=True, upload_to="static/img/avatars")
