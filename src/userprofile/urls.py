from django.contrib import admin
from django.urls import include, path
from .views.edit_profile import EditProfileView
from .views.settings import EditSettingsView
from .views.two2fa import get_otp_view, get_otp

urlpatterns = [
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('2fa/', get_otp_view, name='2fa'),
    path('get-otp/', get_otp, name='get-otp'),
    path('settings/', EditSettingsView.as_view(), name='settings'),
]
