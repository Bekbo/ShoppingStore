from django.urls import path
from rest_framework import routers

from .views import ProductViewSet, CommentViewSet, Orders, make_order

router = routers.SimpleRouter()
router.register('products', ProductViewSet)
router.register('comments', CommentViewSet)
router.register('orders', Orders)
urlpatterns = [
    path("ok", make_order)
]
urlpatterns += router.urls
