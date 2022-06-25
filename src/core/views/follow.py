from calendar import c
import re
from django.views.generic import View
from ..models import _Post
from userprofile.models import _UserProfileModel
from django.http import JsonResponse
from django.contrib.auth.models import User
from notifications.signals import notify
from core.templatetags.custom_tag import get_notifications

class FollowUsers(View):
    def get(self, request,):
        current_user = User.objects.get(username=request.user)
        followed_user = User.objects.get(username=request.GET.get('followeduser'))
        current_user_profile = _UserProfileModel.objects.get(user=current_user)
        followed_user_profile = _UserProfileModel.objects.get(user=followed_user)

        for user in current_user_profile.following.all():
            if user == followed_user:
                current_user_profile.following.remove(followed_user)
                followed_user_profile.followers.remove(current_user)
                followed_user_profile.save()
                current_user_profile.save()
                followcount = followed_user_profile.followers.count()
                user.notifications.filter(verb=f"follow#{request.user}_{followed_user_profile.user}").delete()
                notification = get_notifications(request.user)
                return JsonResponse({
                    'status': 'unfollowed', 
                    'message': 'Follow' ,
                    'followcount':str(followcount),
                    'notification': notification,
                    'followcount_message':str(followcount) + ' followers',
                    })

        current_user_profile.following.add(followed_user)
        followed_user_profile.followers.add(current_user)

        followed_user_profile.save()
        current_user_profile.save()
        followcount = followed_user_profile.followers.count()

        if current_user != followed_user_profile.user:
            notify.send(    
                current_user, 
                recipient=followed_user_profile.user, 
                verb=f'follow#{request.user}_{followed_user_profile.user}', 
                description=f'{request.user} followed you',
                
                )
        notification = get_notifications(request.user)

        return JsonResponse({
        'status': 'followed', 
        'message': 'Following', 
        'followcount':str(followcount),
        'notification': notification,  
        'followcount_message':str(followcount) + ' followers',})
