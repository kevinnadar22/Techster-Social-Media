# Profile View
from django.contrib import messages
from django.shortcuts import render
from userprofile.models import _UserProfileModel
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from userprofile.forms import UserProfileForm
from django.contrib.auth.models import User
from ..models import _Post
from django.db.models import Q

@method_decorator(login_required(login_url='login'), name='dispatch')
class SearchUserView(ListView):
    model = User
    template_name = 'core/search_user.html'
    context_object_name = 'users'

    def get_queryset(self): # new
        if 'q' in self.request.GET:
            query = self.request.GET.get('q')

            results = User.objects.filter(
                Q(username__icontains=query) | 
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
                )
            result_user = []
            for user in results:
                users = _UserProfileModel.objects.get(user=user)
                result_user.append(users)

            if len(result_user) > 0:
                return result_user
                
            result_user = None
            return result_user


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'q' in self.request.GET:
            context["title"] = f"Searched for {self.request.GET['q']}"
            context["query"]= self.request.GET['q']
            return context

        context["title"] = 'Search user'