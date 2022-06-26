from django.shortcuts import render
from django.views.generic import View
from ..models import _Post
from userprofile.models import _UserProfileModel
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class PostDetailView(DetailView):
    model = _Post
    
    template_name = "core/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        id = self.kwargs.get('uuid') or self.request.GET.get('uuid') or None
        queryset = queryset.filter(id=id)
        obj = queryset.get()
        return obj
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('uuid') or self.request.GET.get('uuid') or None
        user_profile = _UserProfileModel.objects.get(user=self.request.user)
        user_following = user_profile.following.all()
        context["users_to_follow"] = _UserProfileModel.objects.all().exclude(user__in=user_following)

        if _Post.objects.get(id=id).is_comment_disabled == False:
                context["comments"] = _Post.objects.get(id=id).comments.all().order_by('-date_created')
        return context
