from django.db import models 

class PostTag(models.Model):

    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="related_post")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="related_tag")