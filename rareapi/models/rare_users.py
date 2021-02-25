from django.db import models
from django.contrib.auth.models import User
from rareapi.models.subscriptions import Subscription


class RareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=200)
    created_on = models.DateTimeField()
    active = models.BooleanField()

    # Returns custom property subscriptions for RareUser where subscriptions follower field=self.
    @property
    def subscriptions(self):
        subs = Subscription.objects.filter(follower=self)
        return subs

    