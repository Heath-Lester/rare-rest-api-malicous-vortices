from django.db import models


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    created_on = models.DateField()

    @property
    def my_comment(self):
        return self.__my_comment

    @my_comment.setter
    def my_comment(self, value):
        self.__my_comment = value