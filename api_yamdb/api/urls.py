"""api_urls."""
from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, ReviewViewSet, UserViewSet
from users.views import send_auth_token, send_confirmation_code

from .views import CategoryViewSet, GenresViewSet, TitlesViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router_v1.register(r'users', UserViewSet, basename='users')

router_v1.register(
    r'categories',
    CategoryViewSet, basename='categories')
router_v1.register(
    r'genres',
    GenresViewSet, basename='genres')
router_v1.register(
    r'titles',
    TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', send_confirmation_code, name='singup'),
    path('v1/auth/token/', send_auth_token, name='token'),
]
