from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from userprofile.models import _OTPModel, _UserProfileModel

# Login View
def login_view(request):
    """
    If the user is already logged in, redirect to the home page. If the user is not logged in, check if
    the request method is POST. If it is, check if the request is for login or otp. If it is for login,
    authenticate the user and if the user is authenticated, check if the user has enabled 2FA. If the
    user has enabled 2FA, render the 2FA login page. If the user has not enabled 2FA, log the user in
    and redirect to the home page. If the request is for otp, check if the otp is valid and if it is,
    log the user in and redirect to the home page. If the request method is not POST, render the login
    page
    
    :param request: The request object
    :return: A render of the login.html page
    """
    if request.user.is_authenticated:
        return redirect('home')

    # Post Method
    if request.method == 'POST':
        if "login" in request.POST:
            data = request.POST.dict()
            user = authenticate(
                username=data['username'],
                password=data['password']
            )

            if user is not None:
                user_profile, _ = _UserProfileModel.objects.get_or_create(user=user)
                context = {'profile': user_profile}
                if user_profile.is_2fa:
                    messages.success(request, "Two Factor Authentication has been enabled",)
                    return render(request, 'auth/2falogin.html', context=context)
                else:
                    login(request, user)
                    messages.success(request, "Logged in!",)
                    return redirect(settings.REDIRECT_AFTER_LOGIN)
            else:
                messages.error(request, "Invalid Username or Password",)

        if 'otp' in request.POST:
            otp = request.POST.get('otp')
            phone = request.POST.get('phone')
            otp_obj = _OTPModel.objects.get(otp=otp)

            user = _UserProfileModel.objects.get(phone=phone)
            if otp_obj.is_verified:
                messages.error(request, 'OTP expired')

            if otp_obj.is_expired:
                messages.error(request, 'OTP expired')

            otp_obj.is_verified = True
            otp_obj.save()
            
            # This is a way to login a user without a password.
            login(request, user.user, backend='django.contrib.auth.backends.ModelBackend')
            # This is a way to display a message to the user.
            messages.success(request, "Logged in!",)
            return redirect(settings.REDIRECT_AFTER_LOGIN)

    return render(request, 'auth/login.html', context={'is_social': settings.SOCIAL_LOGIN_BOOL})