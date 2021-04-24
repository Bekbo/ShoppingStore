from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import mixins, viewsets, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.serializers import ProductSerializer
from auth_ import serializers
from auth_.models import User
from auth_.serializers import UserSerializer, RegisterUserSerializer, RegisterSellerSerializer, SellerSerializer


@csrf_exempt
def auth(request):
    jwt_authentication = JSONWebTokenAuthentication()
    authenticated = jwt_authentication.authenticate(request)
    user = authenticated[0]
    return HttpResponse(user)


class UserRegisterView(generics.GenericAPIView):

    def get_serializer_class(self):
        return RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                ser = UserSerializer(instance=user)
                return HttpResponse(ser.data)
            else:
                return HttpResponse('invalid')
                pass
        except Exception as e:
            return HttpResponse('err')


class SellerRegisterView(generics.GenericAPIView):

    def get_serializer_class(self):
        return RegisterSellerSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterSellerSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                ser = SellerSerializer(instance=user)
                return HttpResponse(ser.data)
            else:
                return HttpResponse('invalid')
                pass
        except Exception as e:
            return HttpResponse('err')
