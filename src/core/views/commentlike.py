from django.views.generic import View
from ..models import _Comments, _Post
from django.http import JsonResponse

class LikeComment(View):
    def get(self, request,):
        id = request.GET.get('id')
        current_user = request.user
        liked_users = _Comments.objects.get(id=id).comment_like.all()

        for user in liked_users:
            if user == current_user:
                _Comments.objects.get(id=id).comment_like.remove(user)
                message = _Comments.objects.get(id=id).comment_like.all().count()
                return JsonResponse({'status': 'disliked', 'message': message})

        _Comments.objects.get(id=id).comment_like.add(request.user)

        count =  _Comments.objects.get(id=id).comment_like.all().count()

        return JsonResponse({'status': 'liked', 'message': count})
        



