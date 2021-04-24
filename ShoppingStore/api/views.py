from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from requests import Response
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
import json
from auth_.serializers import UserSerializer
from .models import Product, Comment
from .serializers import ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer, CommentSerializer, \
    CommentCreateSerializer
from auth_.models import User
from auth_.roles import SellerPermission


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    @action(methods=['GET'], detail=False, url_path='main', url_name='list',
            permission_classes=(AllowAny,))
    def products(self, request):
        serializer = ProductSerializer(Product.objects.all(), many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    @action(methods=['POST'], detail=False, url_path='add', url_name='create',
            permission_classes=(SellerPermission,))
    def post_product(self, request):
        data = self.request.data
        serializer = ProductCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('Invalid Product')

    @action(methods=['PUT', 'DELETE'], detail=True, url_path='edit', url_name='update',
            permission_classes=(SellerPermission,))
    def update_product(self, request, pk):
        serializer = ProductUpdateSerializer(instance=self.queryset.get(id=pk), data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.data)

    @action(methods=['POST'], detail=True, url_path='comment', url_name='create',
            permission_classes=(IsAuthenticated,))
    def post_comment(self, request, pk):
        data = self.request.data
        product = Product.objects.get(id=pk)
        serializer = CommentCreateSerializer(data=data, context={'request': request, 'product': product})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response("Comment is not valid!")


class CommentViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(methods=['POST'], detail=True, url_path='add', url_name='create',
            permission_classes=(IsAuthenticated,))
    def post_comment(self, request):
        data = self.request.data
        serializer = CommentCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('Invalid Product')
