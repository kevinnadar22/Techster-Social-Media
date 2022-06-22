from django.db import models
import datetime
from datetime import timezone
from django.contrib.auth.models import User

class OTPModel(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    otp = models.IntegerField(unique=True)
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self): 
        x = self.date_created
        timestamp = x.replace(tzinfo=timezone.utc).timestamp()
        x2 = datetime.datetime.now()
        timestamp2 = x2.replace(tzinfo=timezone.utc).timestamp()
        duration = timestamp2 - timestamp
        if duration > 1200:
            return True
        else: return False

    def __str__(self):
        return self.otp

