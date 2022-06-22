from django.contrib import admin
from django.urls import include, path
from .views.signup import signup
from .views.login import login_view
from .views.logout import logout_view
from .views.home import home
from .views.activate import activate
from .views.pwdchange import change_password
from .views.forgetpwd import forget_password, forget_password_users


urlpatterns = [
    path('', home, name="home"),
    path('signup/', signup, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('change-password/', change_password, name="change_password"),
    path('forget-password/', forget_password, name="forget_password"),
    path('forget-password/users/<uidb64>/<token>/<email_token>/', forget_password_users, name="forget_password_user"),
]

