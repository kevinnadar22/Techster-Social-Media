from django.shortcuts import render
from django.views.generic import View
from ..models import _Post
from userprofile.models import _UserProfileModel
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePage(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    redirect_field_name = 'home'
    model = _Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'core/index.html'
    ordering = ['-date_created']


    def get_context_data(self, **kwargs):

        _UserProfileModel.objects.get_or_create(user=self.request.user)

        context = super().get_context_data(**kwargs)
        user_profile = _UserProfileModel.objects.get(user=self.request.user)
        user_following = user_profile.following.all()
        context["users_to_follow"] = _UserProfileModel.objects.all().exclude(user__in=user_following)

        return context
    
