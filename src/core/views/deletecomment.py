from django.views.generic import View
from ..models import _Comments, _Post
from django.http import JsonResponse
from core.templatetags.custom_tag import get_notifications

class DeleteComment(View):
    def get(self, request,):
        comment_id = request.GET.get('comment')
        user = self.request.user
        comment = _Comments.objects.get(id=comment_id)

        post = _Post.objects.get(posted_comments=comment)
        if comment.user == user:
            post.user.notifications.filter(verb=f"comment#{comment.id}").delete()
            notification = get_notifications(request.user)
            comment.delete()
            comment.save()
            count = post.comments.count()
            return JsonResponse({
                'status': 'success', 
                'message': 'deleted',
                'count': count,
                'notification': notification})

