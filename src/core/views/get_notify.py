from django.http import JsonResponse
from core.templatetags.custom_tag import get_notifications

def get_notify(request):
    notifications = get_notifications(request.user)
    return JsonResponse(
       ['notifications', notifications,],
       safe=False
    )


