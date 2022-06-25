from calendar import c
from django.views.generic import View
from ..models import _Comments, _Post
from django.http import JsonResponse
from notifications.signals import notify
from core.templatetags.custom_tag import get_notifications

class LikeComment(View):
    def get(self, request,):
        id = request.GET.get('id')
        current_user = request.user
        liked_users = _Comments.objects.get(id=id).comment_like.all()

        for user in liked_users:
            if user == current_user:
                
                my_user = _Comments.objects.get(id=id).user
                comment = _Comments.objects.get(id=id) 
                post = _Post.objects.get(comments=comment)
                string = f"commentlike#{current_user}_{post.id}_{comment.id}"
                my_user.notifications.filter(verb=string).delete()

                _Comments.objects.get(id=id).comment_like.remove(user)
                message = _Comments.objects.get(id=id).comment_like.all().count()

                return JsonResponse({'status': 'disliked', 'message': message})

        _Comments.objects.get(id=id).comment_like.add(request.user)

        count =  _Comments.objects.get(id=id).comment_like.all().count()

        comment = _Comments.objects.get(id=id)
        post = _Post.objects.get(comments=comment)

        if request.user != comment.user:
            notify.send(    
                        request.user, 
                        recipient=comment.user, 
                        verb=f'commentlike#{current_user}_{post.id}_{comment.id}', 
                        description=f'{request.user} liked your comment',
                        )

        return JsonResponse({'status': 'liked', 'message': count})
        



