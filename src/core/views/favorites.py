# Profile View
from django.contrib import messages
from django.shortcuts import render
from userprofile.models import _UserProfileModel
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from userprofile.forms import UserProfileForm
from django.contrib.auth.models import User
from ..models import _Favorite

@method_decorator(login_required(login_url='login'), name='dispatch')
class FavoriteView(View):
    def get(self, request,*args, **kwargs):    
        user = request.user
        user_profile = _UserProfileModel.objects.get(user=user)
        favorite = _Favorite.objects.filter(user=user)
        posts = []
        for post in favorite:  
            posts.append(post.post)

        posts.reverse()

        misc = 'Favorites'
        context = {'profile': user_profile, 'posts':posts, 'user':user, 'misc':misc}
        return render(request, 'core/profile.html', context)
    