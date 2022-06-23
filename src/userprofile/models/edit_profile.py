from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from django_countries.data import COUNTRIES
from cloudinary.models import CloudinaryField

GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]


class UserEditProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_image = CloudinaryField('image', blank = True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True,)
    gender = models.CharField(max_length=255, blank=True, choices=GENDER)
    job = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(blank=True, null=True, max_length=10, unique=True)
    country = models.CharField(max_length=30, blank=True, null=True, default='', choices=sorted(COUNTRIES.items()))
    is_2fa = models.BooleanField(default=False, null=True, blank=True)
    twitter = models.CharField(max_length=30, blank=True, null=True, )
    facebook = models.CharField(max_length=30, blank=True, null=True,)
    instagram = models.CharField(max_length=30, blank=True, null=True, )
    linkedin = models.CharField(max_length=30, blank=True, null=True,)
    is_email_verified = models.BooleanField(default=False, null=True, blank=True,)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):

        if self.phone is not None:
            if str(self.phone).startswith("91"):
                x = str(self.phone).replace("91", "", 1)
                self.phone = x
        
        super(UserEditProfile, self).save(*args, **kwargs)

    @property
    def image_url(self):
        if self.profile_image is None:
            return '/media/default_profile.png'
        return (
            f"https://res.cloudinary.com/kevinnadar/v1655924460/{self.profile_image}"
        )