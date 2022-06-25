"""techster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.views.error import error
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('user/', include('userprofile.urls')),
    path('', include('core.urls')),
    path('error/', error, name='error'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.error.my_custom_page_not_found_view'
handler500 = 'core.views.error.my_custom_error_view'
handler403 = 'core.views.error.my_custom_permission_denied_view'
handler400 = 'core.views.error.my_custom_bad_request_view'