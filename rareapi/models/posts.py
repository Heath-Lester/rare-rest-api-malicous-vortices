from django.db import models
from .rare_users import RareUser

class Post(models.Model):

    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    image_url = models.CharField(max_length=200)
    content = models.CharField(max_length=2500)
    approved = models.BooleanField()

    @property
    def my_post(self):
        return self.__my_post

    @my_post.setter
    def my_post(self, value):
        self.__my_post = value

    @property
    def related_tags(self):
        return self.__related_tags


    # Returns RareUser that matches user id on current post as custom property called author
    @property
    def author(self):
        author = RareUser.object.get(pk=self.user__id)
        return author
    

    @related_tags.setter
    def related_tags(self, value):
        self.__related_tags = value

    @property
    def reactions(self):
        return self.__reactions

    @reactions.setter
    def reactions(self, value):
        self.__reactions = value
