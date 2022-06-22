import re
from django.db import models
from django.contrib.auth.models import User


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    post = models.ForeignKey("core.Post", on_delete=models.CASCADE, related_name="comment_post")
    comment_like  = models.ManyToManyField(User, related_name="comments_like",)
    date_created = models.DateTimeField(auto_now_add=True)  
    comment = models.TextField(blank=True, null=True, )

    def __str__(self):
        return self.comment