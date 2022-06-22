from django.contrib.auth.models import  User
from django.db import models
from ..models import _Post

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(_Post, related_name='favorites', on_delete=models.CASCADE)