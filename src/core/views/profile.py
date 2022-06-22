# Profile View
from django.contrib import messages
from django.shortcuts import render
from userprofile.models import _UserProfileModel
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from userprofile.forms import UserProfileForm
from django.contrib.auth.models import User
from ..models import _Post

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    def get(self, request,*args, **kwargs):    
        user = User.objects.get(username=kwargs['username'])
        user_profile = _UserProfileModel.objects.get(user=user)
        posts = _Post.objects.filter(user=user).order_by('-date_created')
        misc = 'Posts'
        context = {'profile': user_profile, 'posts':posts, 'user':user, 'misc':misc}
        return render(request, 'core/profile.html', context)
