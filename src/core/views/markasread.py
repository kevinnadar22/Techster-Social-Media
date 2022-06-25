from django.http import JsonResponse
from core.templatetags.custom_tag import get_notifications

def mark_as_read(request):
    request.user.notifications.mark_all_as_read()
    notifications = get_notifications(request.user)
    return JsonResponse(
       ['notifications', notifications,],
       safe=False
    )
