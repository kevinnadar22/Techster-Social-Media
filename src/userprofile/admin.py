from django.contrib import admin
from .models import _OTPModel, _UserProfileModel
# Register your models here.

admin.site.register(_OTPModel)
admin.site.register(_UserProfileModel)