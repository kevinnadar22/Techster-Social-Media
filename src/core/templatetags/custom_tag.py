from calendar import c
import re
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
from userprofile.models import _UserProfileModel
from ..models import _Post, _Favorite
from django.contrib.auth.models import User
from django.db.models import Q

@register.simple_tag
def get_profile_image(user):
      user_profile = _UserProfileModel.objects.get(user=user)
      return user_profile.profile_image


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