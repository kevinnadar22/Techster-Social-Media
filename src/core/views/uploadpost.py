from calendar import c
from os import rename
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View
from ..models import _Post
from ..forms import PostForm
from userprofile.models import _UserProfileModel

class UploadPost(View):
    def post(self, request,):
        form = PostForm(request.POST, request.FILES or None)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.user_profile = _UserProfileModel.objects.get(user=request.user)
            new_post.save()
            return HttpResponseRedirect("/")
        context = {
        'error_title':'Internal Server Error',
        'status_code': 500,
        'error_message':'Internal Server Error',
    }
        return render(request, 'core/error.html', context=context)


