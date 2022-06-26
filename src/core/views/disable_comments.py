# Profile View
from django.http import HttpResponse, JsonResponse
from core.models import _Post
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

@method_decorator(login_required(login_url='login'), name='dispatch')
class DisableCommentsView(View):
    def get(self, request,*args, **kwargs):    
        user = request.user
        post_id = request.GET.get('post_id', None)

        post = _Post.objects.get(id=post_id)
        if post.user == user:
            if post.is_comment_disabled  is True:
                post.is_comment_disabled = False
                html = '''                                <div style="cursor: pointer;" class="p-2 rounded-full text-black">
                                    <i class="fa-solid fa-comment-slash"></i>  
                           
                                </div>
                                <span>Disable</span>'''
                post.save()
                return JsonResponse({
                    'html': mark_safe(html),
                })

            else:
                post.is_comment_disabled = True
                html = '''                                <div style="cursor: pointer;" class="p-2 rounded-full text-black">
                                    <i class="fa-solid fa-comment"></i>
                           
                                </div>
                                <span>Enable</span>'''
                post.save()
                return JsonResponse({
                    'html': mark_safe(html),
                })
                

        return HttpResponse('Not authorized to disable comments')