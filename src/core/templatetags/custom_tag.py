from calendar import c
import re
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
from userprofile.models import _UserProfileModel
from ..models import _Post, _Favorite, _Comments
from django.contrib.auth.models import User
from django.db.models import Q

@register.simple_tag
def get_profile_image(user):
      user_profile = _UserProfileModel.objects.get(user=user)
      return user_profile.image_url

@register.simple_tag()
def replace_hash(caption:str):
    content = caption
    arr = re.findall(r"#(\w+)", content)
    for hsh in arr:
        if len(hsh) < 80:
            full_hash = '#' + hsh
            content = content.replace(full_hash, f'<a target="_blank" href="/hashtag/{hsh}/">#{hsh}</a>')

    arr = re.findall(r"@(\w+)", content)
    for hsh in arr:
        if len(hsh) < 80:
            full_hash = '@' + hsh
            content = content.replace(full_hash, f'<a target="_blank" href="/profile/{hsh}">@{hsh}</a>')

    return mark_safe(content)
 
@register.simple_tag()
def liked_by_user(user, id):
    current_user = user
    liked_users = _Post.objects.get(id=id).likes.all()
    for user in liked_users:
        if user == current_user:
            if liked_users.count() > 1:
                return f"Liked by You and {int(liked_users.count()) - 1} others" 
            return "Liked by you"
        

    return liked_users.count()


@register.simple_tag()
def liked_by_user_icon(user, id):
    current_user = user
    liked_users = _Post.objects.get(id=id).likes.all()
    for user in liked_users:
        if user == current_user:
            content = f'<i id="solid#{id}" class="fa-solid fa-heart"></i>'
            return mark_safe(content)
    content = f'<i id="regular#{id}" class="fa-regular fa-heart"></i>' 
    return mark_safe(content)



@register.simple_tag()
def is_social_media(user):
    user_profile = _UserProfileModel.objects.get(user=user)
    facebook = user_profile.facebook
    instagram = user_profile.instagram
    twitter = user_profile.twitter
    linkedin = user_profile.linkedin
    content = ''
    html = '<a target="_blank" href="https://social.com/%s" class="social"><i class="bi bi-social"></i></a>'

    if facebook:
        if len(facebook) > 5:
            content += html.replace('social', "facebook") % facebook

    if instagram:
        if len(instagram) > 5:
            content += html.replace('social', "instagram") % instagram

    if twitter:
        if len(twitter) > 5:
            content += html.replace('social', "twitter") % twitter
    
    if linkedin:
        if len(linkedin) > 5:
            content += html.replace('social', "linkedin") % linkedin

    return mark_safe(content)

@register.simple_tag()
def is_following(current_user, follow_user):
    current_user1 = User.objects.get(username=current_user)
    followed_user1 = User.objects.get(username=follow_user)
    current_user_profile = _UserProfileModel.objects.get(user=current_user1)
    followed_user_profile = _UserProfileModel.objects.get(user=followed_user1)

    for user in current_user_profile.following.all():
        if user == followed_user1:
            return "Following"
    
    return "Follow"

@register.simple_tag()
def is_favorites(user, post_id):
    post = _Post.objects.get(id=post_id)
    if _Favorite.objects.filter(Q(user=user) & Q(post=post)).exists():
        return "Remove Favorites"
    return "Add Favorites"


@register.simple_tag()
def is_favorites_icon(user, post_id):
    post = _Post.objects.get(id=post_id)
    if _Favorite.objects.filter(Q(user=user) & Q(post=post)).exists():
        return mark_safe('<i class="fa-solid fa-star"></i>')
    return mark_safe('<i class="fa-regular fa-star"></i>')


@register.simple_tag()
def get_notifications(user):

    unread_notifications = user.notifications.unread() 
    read_notifications = user.notifications.read() 

    if len(unread_notifications) > 0:
        context = get_notifications_func(unread_notifications, '#e1e1e1')
    else:
        context  = '''                           <div class="divide-gray-300 divide-gray-50 divide-opacity-50 divide-y px-4 ">
                                <div class="flex items-center justify-between py-3">
                                    <div class="flex flex-1 items-center space-x-4">
                                        No new notifications available
                                    </div></div></div>''' 

    if len(read_notifications) > 0:
        context += get_notifications_func(read_notifications, '')

    return mark_safe(context)


def get_notifications_func(notifications, bgcolor):
    context = ""
    html = ''' <li>
                            <a href="{}" style="background-color: {} !important">
                                <div class="drop_avatar"> <img src={} alt="">
                                </div>
                                <div class="drop_content">
                                    <p> {} </p>
                                
                                <span class="time-ago"> {} ago </span>
                                </div>
                            </a>
                        </li>'''

    if len(notifications) > 0:

        for notification in notifications:
        
            profile = get_profile_image(notification.actor_object_id)

            actor_obj = User.objects.get(id=notification.actor_object_id)
            if notification.recipient == actor_obj:
                pass

            elif 'like' in notification.verb:
                post_id = notification.verb.split('_')[1]
                context += html.format(f'/p/{post_id}', bgcolor, profile, notification.description, notification.timesince())

            elif 'follow' in notification.verb:
                followed_user =  notification.verb.split('_')[0].split('#')[1]
                context += html.format(f'/profile/{followed_user}', bgcolor, profile, notification.description, notification.timesince())

            elif 'comment' in notification.verb:
                post_id =  notification.verb.split('#')[1]
                comment = _Comments.objects.get(id=post_id)
                
                post = _Post.objects.get(posted_comments=comment)
                context += html.format(f'/p/{post.id}', bgcolor, profile, notification.description, notification.timesince())

            elif 'likecomment' in notification.verb:
                post_id =  notification.verb.split('_')[1]
                user = User.objects.get(username=notification.verb.split('_')[0].split('#')[1])
                comment = _Comments.objects.get(id=post_id)
                post = _Post.objects.get(posted_comments=comment)
                context += html.format(f'/p/{post.id}', bgcolor, profile, notification.description, notification.timesince())


    return context

@register.filter
def order_comment(post):
    if post.comments is not None:
        comment = post.comments.all().order_by('-date_created')[:2]
        return comment



@register.filter
def order_follower_users(user_profile, current_user):
    current_user_profile = _UserProfileModel.objects.get(user=current_user)
    user_profile = _UserProfileModel.objects.get(user=user_profile)
    
    for user in current_user_profile.followers.all():
        for user_p in user_profile.followers.all():
            if user_p == user:
                print(user_p)