from pydoc import describe
from django.views.generic import View
from ..models import _Post
from django.http import JsonResponse
from notifications.signals import notify
from django.contrib.auth.models import User
from core.templatetags.custom_tag import get_notifications
# 
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
                user = post.user
                user.notifications.filter(verb=f"like#{request.user}_{post.id}").delete()
                notification = get_notifications(request.user)
                return JsonResponse({'status': 'disliked', 'message': message, 'notification': notification})

        post.likes.add(request.user)
        count =  _Post.objects.get(id=id).likes.all().count()
        message =  f'Liked by you and {count - 1} others'
        if count - 1 == 0:
            message =  f'Liked by you'

        if current_user != post.user:
            notify.send(    
                current_user, 
                recipient=post.user, 
                verb=f'like#{request.user}_{post.id}', 
                description=f'{request.user} liked your post',
                
                )
                
        notification = get_notifications(request.user)
        return JsonResponse({'status': 'liked', 'message': message, 'notification': notification})
        



