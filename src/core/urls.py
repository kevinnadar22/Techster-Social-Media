from django.urls import reverse, path, include
from .views.homeview import HomePage
from .views.uploadpost import UploadPost
from .views.postcomment import PostComment
from .views.like import LikePost
from .views.commentlike import LikeComment
from .views.follow import FollowUsers
from .views.profile import ProfileView
from .views.post_detail import PostDetailView
from .views.deletecomment import DeleteComment
from .views.favorites import FavoriteView
from .views.createfav import CreateFavoriteView
from .views.del_post import DeletePost
from .views.search_user import SearchUserView
from .views.edit_post import EditPostView
from .views.hashtag import HashtagPostView
from .views.get_notify import get_notify
from .views.markasread import mark_as_read
from .views.disable_comments import DisableCommentsView


urlpatterns = [
    path('', HomePage.as_view(), name="home"),
    path('upload-post/', UploadPost.as_view(), name="upload_post"),
    path('post-comment/', PostComment.as_view(), name="post_comment"),
    path('like-post/', LikePost.as_view(), name="like_post"),
    path('like-comment/', LikeComment.as_view(), name="like_comment"),
    path('followusers/', FollowUsers.as_view(), name="followusers"),
    path('p/<str:uuid>/', PostDetailView.as_view(), name="post_detail"),
    path('edit/<str:uuid>/', EditPostView.as_view(), name="edit_post"),
    path('deletecomment/', DeleteComment.as_view(), name="deletecomment"),
    path('favorites/', FavoriteView.as_view(), name="favorite_view"),
    path('createfavorite/', CreateFavoriteView.as_view(), name="makefavorite"),
    path('deletepost/', DeletePost.as_view(), name="deletepost"),
    path('search/', SearchUserView.as_view(), name="search_user"),
    path('hashtag/<str:hashtag>/', HashtagPostView.as_view(), name="hastag"),
    path('getnotify/', get_notify, name="getnotify"),
    path('markasread/', mark_as_read, name="mark_as_read"),
    path('disable-comments/', DisableCommentsView.as_view(), name="disable_comments"),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]

