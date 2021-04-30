from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import mixins, viewsets, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.serializers import ProductSerializer
from auth_ import serializers
from auth_.models import User
from auth_.roles import CustomerPermission, SellerPermission
from auth_.serializers import UserSerializer, RegisterUserSerializer, RegisterSellerSerializer, SellerSerializer, \
    ProfileSerializer
import logging
logger = logging.getLogger('authorization')


@csrf_exempt
def auth(request):
    jwt_authentication = JSONWebTokenAuthentication()
    authenticated = jwt_authentication.authenticate(request)
    user = authenticated[0]
    ser = ProfileSerializer(user.profile)
    print(user.pk)
    return JsonResponse(ser.data)


class UserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                logger.info(f"{user.username} registered")
                ser = UserSerializer(instance=user)
                return HttpResponse(ser.data)
            else:
                print(serializer.errors)
                logger.error(serializer.errors)
                return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"{e} error")
            return HttpResponse(e, status=status.HTTP_404_NOT_FOUND)


class SellerRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSellerSerializer
    # permission_classes = (IsAuthenticated,)

    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        if request.user.is_seller:
            logger.warning(f"{request.user} already seller")
            return HttpResponse("You are already a seller", status=status.HTTP_208_ALREADY_REPORTED)
        try:
            serializer = RegisterSellerSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info(f"{request.user} is now seller")
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.info(f"{serializer.errors}")
                return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return HttpResponse(str(e), status=status.HTTP_404_NOT_FOUND)

    @permission_classes(SellerPermission,)
    def put(self, request, *args, **kwargs):
        user = request.user
        if user.seller.is_active:
            user.seller.make_inactive()
            logger.info(f"{user} is not selling now")
            return HttpResponse('Your shop is inactive', status=status.HTTP_200_OK)
        else:
            user.seller.make_active()
            logger.info(f"{user} is selling now")
            return HttpResponse('Your shop is active', status=status.HTTP_200_OK)

    @permission_classes(SellerPermission,)
    def delete(self, request, *args, **kwargs):
        request.user.remove_seller()
        logger.info(f"{request.user} close his/her shop")
        return HttpResponse('ok', status=status.HTTP_200_OK)

