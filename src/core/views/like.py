from django.views.generic import View
from ..models import _Post
from django.http import JsonResponse

class LikePost(View):
    def get(self, request,):
        id = request.GET.get('id')
        current_user = request.user
        liked_users = _Post.objects.get(id=id).likes.all()
        post = _Post.objects.get(id=id)

        
        for user in liked_users:
            if user == current_user:
                _Post.objects.get(id=id).likes.remove(user)
                message = _Post.objects.get(id=id).likes.all().count()
                return JsonResponse({'status': 'disliked', 'message': message})

        post.likes.add(request.user)
        count =  _Post.objects.get(id=id).likes.all().count()
        message =  f'Liked by you and {count - 1} others'
        if count - 1 == 0:
            message =  f'Liked by you'
        return JsonResponse({'status': 'liked', 'message': message})
        



