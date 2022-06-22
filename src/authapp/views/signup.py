from django.shortcuts import redirect, render
from ..utils import AuthenticationUtils, send_email
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import _Tokens
from django.conf import settings


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        data = request.POST.dict()
        
        validate_data = AuthenticationUtils(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            cpassword=data['cpassword'],
            request=request,
        )

        if validate_data.username_validation() and validate_data.password_validation() and validate_data.email_validation():

            messages.success(
                request, 'Account Created, Confirmation link has sent to your Email',)
        

            # Create User
            user = User.objects.create(
                username = data['username'], 
                email = data['email'],)
            user.set_password(data['password'])
            user.is_active = False
            user.save()
            

            # Confirm Email
            subject = 'Activate your account'
            email_token = send_email(
                request=request,
                user=user,
                subject=subject,
                email_template='auth/email_confirmation.html',
                )

            auth_token = _Tokens.objects.create(token=email_token)
            auth_token.save()

            return redirect(settings.REDIRECT_AFTER_SIGNUP)
        return redirect('signup')



    return render(request, "auth/signup.html", context={'is_social': settings.SOCIAL_LOGIN_BOOL})
