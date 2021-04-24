from rest_framework import serializers
from api.models import Product
from .models import User, Seller, Profile


class ProductSimplestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'age', 'gender', 'cardDetails', 'location', 'is_seller']


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'location', 'is_seller']


class UserSimplestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class SellerSimpleSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Seller
        fields = ['shopName', 'location', 'user']


class SellerSerializer(UserSerializer):
    user = UserSerializer()

    class Meta:
        model = Seller
        fields = ['user', 'shopName', 'location', 'shopEmail']


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'age', 'gender', 'cardDetails', 'location')

    def create(self, validated_data):
        user = User.users.create_user(username=validated_data['username'],
                                      password=validated_data['password'],
                                      email=validated_data['email'],
                                      location=validated_data['location'],
                                      age=validated_data['age'],
                                      gender=validated_data['gender'],
                                      cardDetails=validated_data['cardDetails'],
                                      is_seller=False)
        return user


class RegisterSellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Seller
        fields = ('user', 'shopEmail', 'shopName')

    def create(self, validated_data):
        user = User.users.create_user(username=validated_data['user'].get('username'),
                                      password=validated_data['user'].get('password'),
                                      email=validated_data['user'].get('email'),
                                      location=validated_data['user'].get('location'),
                                      age=validated_data['user'].get('age'),
                                      gender=validated_data['user'].get('gender'),
                                      cardDetails=validated_data['user'].get('cardDetails'),
                                      is_seller=validated_data['user'].get('is_seller'),
                                      shopName=validated_data['shopName'],
                                      shopEmail=validated_data['shopEmail'])
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSimplestSerializer(read_only=True)
    products = ProductSimplestSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'products']
