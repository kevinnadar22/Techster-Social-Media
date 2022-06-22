# Profile View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authapp.utils import AuthenticationUtils, send_email
from authapp.models import _Tokens
from userprofile.models import _UserProfileModel

@method_decorator(login_required(login_url='login'), name="dispatch")
class EditSettingsView(View):

    def post(self, request):
        if 'settings' in request.POST:
            data = request.POST.dict()
            changed_username = data.get('username')
            changed_email = data.get('email')
            user = User.objects.get(username=request.user)

            if user.username == changed_username and user.email == changed_email:
                messages.success(request, 'Saved changes sucessfully')
            
            if user.username != changed_username or user.email != changed_email:
                validation = AuthenticationUtils(
                    username=changed_username, 
                    email=changed_email, 
                    request=request, 
                    user=user)

                if user.username != changed_username:
                    username_validation = validation.username_validation()
                    if username_validation:
                        user.username = changed_username
                        messages.success(request, 'Saved successfully')

                if user.email != changed_email:
                    email_validation = validation.email_validation()
                    if email_validation:     
                        user.email = changed_email
                        user.is_active = True
                        user_profile = _UserProfileModel.objects.get(user=user)
                        user_profile.is_email_verified = False
                        messages.success(request, 'Verify your new email')
                        user_profile.save()
                        
            user.save()
            return HttpResponseRedirect('/user/edit-profile/')

        if 'verify_email' in request.POST:
            subject = 'Activate your account'
            user = request.user
            email_token = send_email(
                request=request,
                user=user,
                subject=subject,
                email_template='auth/email_confirmation.html',
                )

            auth_token = _Tokens.objects.create(token=email_token)
            auth_token.save()
            messages.success(request, 'Verification link has been sent successfully')
            return HttpResponseRedirect('/user/edit-profile/')

            

