from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import auth
urlpatterns = [
    path('auth/', obtain_jwt_token)
]