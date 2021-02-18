from django.db import models

class Subscription(models.Model):

    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rareusers_follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rareusers_author")
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    ended_on = models.DateTimeField(auto_now=False, auto_now_add=False)