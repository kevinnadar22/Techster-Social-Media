# Profile View
from django.contrib import messages
from django.shortcuts import render
from userprofile.models import _UserProfileModel
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from userprofile.forms import UserProfileForm
from django.contrib.auth.models import User
from ..models import _Post
from django.db.models import Q

@method_decorator(login_required(login_url='login'), name='dispatch')
class HashtagPostView(View):
    def get(self, request, *args, **kwargs): # new
        _UserProfileModel.objects.get_or_create(user=self.request.user)
        hashtag = kwargs['hashtag']
        posts = _Post.objects.filter(caption__contains=f"#{hashtag}").order_by('-date_created')
        user_profile = _UserProfileModel.objects.get(user=self.request.user)
        user_following = user_profile.following.all()
        context = {'posts': posts, 'hashtag': hashtag}
        context["users_to_follow"] = _UserProfileModel.objects.all().exclude(user__in=user_following)
        return render(request, 'core/index.html', context)


