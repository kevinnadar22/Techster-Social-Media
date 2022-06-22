from ..models import _Post
from userprofile.models import _UserProfileModel
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import PostForm

class EditPostView(LoginRequiredMixin, UpdateView):
    model = _Post
    form_class = PostForm
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
        context['misc'] = 'edit_post'
        return context
