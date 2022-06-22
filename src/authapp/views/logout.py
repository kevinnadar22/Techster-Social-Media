from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Login View
@login_required(login_url='signup')
def logout_view(request):

    logout(request)
    messages.success(request, "Logged Out!")
    return redirect(settings.REDIRECT_AFTER_LOGOUT)

