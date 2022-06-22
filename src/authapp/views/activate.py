from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from ..tokens import generate_token
from ..models import _Tokens
from ..utils import *
from userprofile.models import _UserProfileModel


# Activate Email View
def activate(request, uidb64, token):

    auth_token = _Tokens.objects.get(token=token)
    
    if auth_token.is_expired == True:
        messages.error(
            request, "Link Expired",)
        return redirect('login')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generate_token.check_token(my_user, token):
        my_user.is_active = True

        user_profile, __ = _UserProfileModel.objects.get_or_create(user=my_user)
        user_profile.is_email_verified = True
        user_profile.save()
        
        my_user.save()
        messages.success(request, "Email has been verified",
                         )
        auth_token.is_expired = True
        auth_token.save()
        return redirect('/auth/login/')

