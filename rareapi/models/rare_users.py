from django.db import models
from django.contrib.auth.models import User


class RareUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=200)
    created_on = models.DateTimeField()
    active = models.BooleanField()