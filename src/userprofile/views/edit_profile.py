# Profile View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import _UserProfileModel, _OTPModel
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..forms import UserProfileForm
from django.contrib.auth.models import User

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = _UserProfileModel.objects.get_or_create(user=request.user)
        self.phone = self.profile.phone
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserProfileForm(instance=self.profile)
        context = {'profile': self.profile, 'form':form}
        return render(request, 'user/profile.html', context)

    def post(self, request):
  
        form = UserProfileForm(request.POST, request.FILES, instance=self.profile)
        if form.is_valid():
            if form.cleaned_data.get('phone') != self.phone:
                  self.profile.is_2fa = False
                  
            profile = form.save(commit=False)

            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']

            if 'delete' in request.POST:
                profile.profile_image = None

            profile.user = self.request.user
            profile.save()
            self.profile.save()

            # User Model
            user = User.objects.get(username=self.request.user)


            if profile.first_name is not None:
                user.first_name = profile.first_name

            if profile.last_name is not None:
                user.last_name = profile.last_name

            user.save()

            messages.success(request, 'Saved Successfully')
            
            form = UserProfileForm(instance=self.profile)
            context = {'profile':self.profile, 'form':form}
            return render(request, 'user/profile.html', context)

        else:
           
            if form.errors:
                for field in form:
                    for error in field.errors:
                        error_message = error
            messages.error(request, error_message)
            profile, __ = _UserProfileModel.objects.get_or_create(user=request.user)
            form = UserProfileForm(instance=profile)

            context = {'profile': profile, 'form':form}
            return render(request, 'user/profile.html', context)
