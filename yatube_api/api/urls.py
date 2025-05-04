"""
URL конфигурация для API приложения Yatube.

В этом модуле регистрируются маршруты для ViewSet-ов и аутентификационные
эндпоинты, предоставляемые Djoser.
"""

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet

router = SimpleRouter()
router.register("groups", GroupViewSet)
router.register("posts", PostViewSet)
router.register("follow", FollowViewSet, basename="follow")
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]
