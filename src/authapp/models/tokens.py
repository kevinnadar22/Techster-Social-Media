from django.db import models

class Tokens(models.Model):
    token = models.CharField(unique=True, max_length=120)
    is_expired = models.BooleanField(default=False)
