# Profile View
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import _Favorite, _Post
from django.http import JsonResponse
from django.db.models import Q
from ..templatetags.custom_tag import is_favorites_icon, is_favorites

@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateFavoriteView(View):
    def get(self, request,*args, **kwargs):    
        user = request.user
        post_id = request.GET.get('post_id', None)
        post = _Post.objects.get(id=post_id)

        if _Favorite.objects.filter(Q(user=user) & Q(post=post)).exists():
            x = _Favorite.objects.filter(Q(user=user) & Q(post=post)).delete()
            html = get_html(user, post_id)
            return JsonResponse(
            {
                'status': 'success',
                'message': 'deleted',
                'html': html
            }
        )

        
        x = _Favorite.objects.create(user=user, post = post)
        x.save()
        html = get_html(user, post_id)
        return JsonResponse(
            {
                'status': 'success',
                'message': 'added'  ,
                'html': html  
            }
        )
        
    

def get_html(user, post_id):
    is_favorite_icon = is_favorites_icon(user, post_id)
    is_favorite = is_favorites(user, post_id)
    html = f'''<div style="cursor: pointer;" class="p-2 rounded-full text-black ">
                                       {is_favorite_icon}
                                            
                                            </div>

                                    <span>{is_favorite}</span>'''

    return html