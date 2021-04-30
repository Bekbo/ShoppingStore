from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from requests import Response
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
import json
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from auth_.serializers import UserSerializer
from .models import Product, Comment, Order
from .serializers import ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer, CommentSerializer, \
    CommentCreateSerializer, CategorySerializer, OrderSerializer
from auth_.models import User
from auth_.roles import SellerPermission
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from auth_.roles import SellerPermission, CustomerPermission
import logging
logger = logging.getLogger('api')


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.actual()
    permission_classes = (AllowAny,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination

    # Can be removed
    @action(methods=['GET'], detail=False, url_path='main', url_name='list',
            permission_classes=(AllowAny,))
    def products(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def list(self, request, *args, **kwargs):
        serializer = ProductSerializer(self.queryset, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    @action(methods=['POST'], detail=False, url_path='add', url_name='create',
            permission_classes=(SellerPermission,))
    def post_product(self, request):
        try:
            data = self.request.data
            serializer = ProductCreateSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info(f"{request.user} created {serializer.data['name']}")
                return JsonResponse(serializer.data)
            else:
                logger.error(f"{request.user} try to post product with bad request")
                return HttpResponse('Invalid Product', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"{e}")
            return HttpResponse(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['PUT', 'DELETE'], detail=True, url_path='edit', url_name='update',
            permission_classes=(IsAuthenticated, SellerPermission))
    def update_product(self, request, pk):
        if request.method == "PUT":
            product = self.queryset.get(id=pk)
            serializer = ProductUpdateSerializer(instance=product, data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"{request.user} updated {product}")
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.data)
        elif request.method == "DELETE":
            product = self.queryset.get(id=pk)
            if product.seller == request.user.seller:
                product.delete()
                return HttpResponse('deleted')
            else:
                return HttpResponse('You can delete only your products!')

    @action(methods=['POST'], detail=True, url_path='comment', url_name='create',
            permission_classes=(IsAuthenticated,))
    def post_comment(self, request, pk):
        data = self.request.data
        print(data)
        product = Product.objects.get(id=pk)
        serializer = CommentCreateSerializer(data=data, context={'request': request, 'product': product})
        print(serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse("Comment is not valid!")

    @action(methods=['GET'], detail=True, url_path='comments', url_name='list',
            permission_classes=(IsAuthenticated,))
    def get_comments(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = CommentSerializer(product.comments.all(), many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(methods=['POST'], detail=False, url_path='category', url_name='create',
            permission_classes=(SellerPermission,))
    def post_category(self, request):
        data = self.request.data
        serializer = CategorySerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response("Category name is not valid!")


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


def make_order(request):
    jwt_authentication = JSONWebTokenAuthentication()
    authenticated = jwt_authentication.authenticate(request)
    user = authenticated[0]
    print(user)
    print(user.has_perm(SellerPermission))
    return HttpResponse("ok")


class Orders(viewsets.GenericViewSet,
             mixins.ListModelMixin,
             mixins.RetrieveModelMixin
             ):
    permission_classes = (AllowAny,)
    queryset = Order.orders.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        serializer = OrderSerializer(self.queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(methods=['GET'], detail=True,
            permission_classes=(AllowAny,))
    def view(self, request, pk):
        print('orders')
        serializer = OrderSerializer(Order.orders.get(id=pk))
        data = serializer.data
        return JsonResponse(data, safe=False)

    @action(methods=['POST'], detail=False, url_path='make',
            permission_classes=(IsAuthenticated,))
    def make_order(self, request):
        print(request.user)
        return HttpResponse('ok')
