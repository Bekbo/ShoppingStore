from django.urls import path
from rest_framework import routers

from .views import ProductViewSet, CommentViewSet
router = routers.SimpleRouter()
router.register('products', ProductViewSet)
router.register('comments', CommentViewSet)
urlpatterns = [
]
urlpatterns += router.urls
