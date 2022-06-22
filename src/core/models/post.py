import re
from django.db import models
from django.contrib.auth.models import User
import uuid

from django.urls import reverse
from userprofile.models import _UserProfileModel

class Post(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "post_images")
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes", )
    comments = models.ManyToManyField("core.Comments", related_name="post_comments", blank=True,)
    caption = models.TextField(blank=True, null=True, help_text="Description")
    user_profile = models.ForeignKey(_UserProfileModel, related_name="user_profile", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.id.__str__()

    def get_absolute_url(self):      
        return reverse('post_detail', args=[str(self.id)])
