from django.views.generic import View
from ..models import _Comments, _Post
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User

class DeletePost(View):
    def get(self, request,):
        deleted_id = request.GET.get('deleted_post')
        current_user = self.request.user

        user = User.objects.get(username=current_user)
        post = _Post.objects.get(id=deleted_id)

        if post.user == current_user:
            post.delete()

            return JsonResponse({'status': 'success', 'content': 'deleted'})

        else:
            HttpResponseRedirect('/404')


