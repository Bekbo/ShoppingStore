from datetime import datetime

from rest_framework import serializers

from auth_.models import Seller
from auth_.serializers import SellerSerializer, UserSimpleSerializer, SellerSimpleSerializer, UserSimplestSerializer
from .models import Product, ShippingAddress, Category, Comment, Order


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address']


class ProductSellerSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Seller
        fields = ['user', 'shopName', 'location', 'shopEmail', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    location = serializers.IntegerField()
    seller = ProductSellerSerializer(read_only=True)
    is_active = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'amount', 'location', 'seller', 'is_active']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'is_active']


class ProductSimpleSerializer(OrderProductSerializer):
    seller = SellerSimpleSerializer()

    class Meta:
        model = Product
        fields = OrderProductSerializer.Meta.fields + ['seller']


class ProductUpdateSerializer(serializers.ModelSerializer):
    location = serializers.IntegerField()
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Product
        fields = ['description', 'price', 'amount', 'location', 'is_active']

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.location = validated_data.get('location', instance.location)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def delete(self, instance):
        print('delete', instance)
        return instance


class ProductCreateSerializer(serializers.ModelSerializer):
    location = serializers.IntegerField()
    seller = SellerSimpleSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'amount', 'location', 'seller']

    def create(self, validated_data):
        return Product.objects.create(
            name=validated_data['name'],
            category=validated_data['category'],
            description=validated_data['description'],
            price=validated_data['price'],
            amount=validated_data['amount'],
            location=validated_data['location'],
            seller=self.context['request'].user.seller
        )


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSimplestSerializer(read_only=True)
    # product = ProductSimpleSerializer(read_only=True)
    published = serializers.DateField()

    class Meta:
        model = Comment
        fields = ['user', 'title', 'body', 'published']


class CommentCreateSerializer(serializers.ModelSerializer):
    user = UserSimplestSerializer(read_only=True)
    product = ProductSimpleSerializer(read_only=True)
    published = serializers.DateField(required=False)
    title = serializers.CharField()
    body = serializers.CharField()

    class Meta:
        model = Comment
        fields = ['user', 'product', 'published', 'title', 'body']

    def create(self, validated_data):
        print(validated_data)
        comment = Comment.objects.create(
            user=self.context['request'].user,
            product=self.context['product'],
            title=validated_data['title'],
            body=validated_data['body'],
        )
        comment.save()
        return comment


class ShippingAddressSerializer(serializers.Serializer):
    address = serializers.CharField()

    class Meta:
        model = ShippingAddress
        fields = ['address']


class OrderSerializer(serializers.ModelSerializer):
    seller = SellerSimpleSerializer(read_only=True)
    customer = UserSimplestSerializer(read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['seller', 'total', 'customer', 'products', 'date_created', 'shipping_address']
