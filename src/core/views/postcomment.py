import re
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
from ..models import _Post
from ..forms import CommentForm
import uuid
from ..templatetags.custom_tag import get_profile_image
from django.utils.safestring import mark_safe
from notifications.signals import notify
from core.templatetags.custom_tag import get_notifications

class PostComment(View):
    def post(self, request,):
        id = request.POST.get('post')
        form = CommentForm(request.POST or None)
        if form.is_valid():
            id  = uuid.UUID(request.POST.get('post'))

            commented = request.POST.get('comment')
            if len(commented) <= 2:
                return JsonResponse({
                'status': 'failed', 
                'message': 'not a valid comment'}
                )


            post = _Post.objects.get(id=id)
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            post.comments.add(new_comment)
            post.save()
            commented = request.POST.get('comment')

            # HTMl
            profile = get_profile_image(request.user)

            replaced_hash = replace_hash(commented)

            if request.user != post.user:
            
                notify.send(    
                request.user, 
                recipient=post.user, 
                verb=f'comment#{new_comment.id}', 
                description=f'{request.user} commented on your post',
                )

            notification = get_notifications(request.user)

            return JsonResponse({
                'status': 'success', 
                'comment': commented,
                'html': mark_safe(comment_html(profile, replaced_hash, new_comment)),
                'notification': notification}
                )

        return HttpResponse("Error")


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

    return content


def comment_html(profile, commented, new_comment):
    html = f"""
                                        <div id="commentbox#{new_comment.id}" class="flex comment-box">
                                        
                                        <div class="w-10 h-10 rounded-full relative flex-shrink-0">
                                            <img src="{profile}" alt="" class="absolute h-full rounded-full w-full">
                                        </div>
                                        <div class="w-full text-gray-700 py-2 px-3 rounded-md bg-gray-100 h-full relative lg:ml-5 ml-2 lg:mr-20 ">

                                        
                                   <div>   {commented}  
                                    
                                    <i id="comment#{new_comment.id}" style="cursor: pointer;" class="comment fa-solid fa-thumbs-up"> 
                                     </i> 
                                     <span id="commentlike#{new_comment.id}"> 
                                     
                                     {new_comment.comment_like.count()}
                                     </span>

                                                                          <i id="deletecomment#{new_comment.id}" style="cursor: pointer;" class="right-2 absolute deletecomment fa-solid fa-trash"></i>
                                    
                                   
                                
                                </div>

                                                
                                        <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 "></div>


                                        
                                        </div>


                                    </div>
                                    """
    return html