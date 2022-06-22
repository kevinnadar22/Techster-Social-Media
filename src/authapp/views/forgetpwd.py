from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from ..tokens import generate_token
from ..models import _Tokens
from ..utils import *




def forget_password(request):
    if request.user.is_authenticated:
        return redirect('signup')
    if request.method == 'POST':
        data = request.POST.dict()

        if not User.objects.filter(email=data['email']):
            messages.error(request, 'This Email does not exist')

        else:
            user = User.objects.get(email=data['email'])
            # Email Confirmation
            email_token = send_email(
                request=request,
                user=user,
                subject='Reset your passsword',
                email_template='auth/forget_password_email.html',
                )

            auth_token = _Tokens.objects.create(token=email_token)
            auth_token.save()

            messages.success(
                request, 'Password Reset Link has been sent to your Email')

    return render(request, 'auth/forget_password.html')


def forget_password_users(request, uidb64, token, email_token):

    if request.user.is_authenticated:
        return redirect('home')

    token = _Tokens.objects.get(token=token)
    if token.is_expired:
        messages.error(
            request, "Link Expired",)
        return redirect('login')
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            my_user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            my_user = None
            messages.error(
                request, "Link Expired",)

        if my_user is None and generate_token.check_token(my_user, token):
            return redirect('home')

        # post method
        if request.method == 'POST':
            data = request.POST.dict()

            validate_data = AuthenticationUtils(
        password=data['password'],
        cpassword=data['cpassword'],
        username=request.user.username,
        request=request,
    )


            my_user.set_password(data['password'])
            token.is_expired = True
            token.save()
            my_user.save()
            messages.success(request, "Password Changed Successfully",
                                )
            return redirect('login')

    return render(request, 'auth/forget_password_user_html.html')
