from django.contrib import admin
from .models import _Post, _Comments, _Favorite
# Register your models here.

admin.site.register(_Post)
admin.site.register(_Comments)
admin.site.register(_Favorite)
