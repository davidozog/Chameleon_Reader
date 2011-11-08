from django.db import models
from django.contrib.auth.models import User
from contents.models import Achievement
     
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    age = models.IntegerField()
    achievements = models.ManyToManyField(Achievement)
    language = models.CharField(max_length=50)
