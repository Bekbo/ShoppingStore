from rest_framework import serializers
from api.models import Product
from .models import User, Seller, Profile
from django.core.validators import validate_email


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
    class Meta:
        model = Seller
        fields = ['shopName', 'location', 'shopEmail', 'is_active']


class SellerSerializer(UserSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Seller
        fields = ['user', 'shopName', 'location', 'shopEmail', 'is_active']


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'age', 'gender', 'cardDetails', 'location')

    def validate(self, attrs):
        password = attrs['password']
        if not attrs.__contains__('email'):
            raise serializers.ValidationError('email is required')
        email = attrs['email']
        if not attrs.__contains__('location'):
            raise serializers.ValidationError('location is required')
        if not attrs.__contains__('age'):
            raise serializers.ValidationError('age is required')
        if not attrs.__contains__('gender'):
            raise serializers.ValidationError('gender is required')
        if not attrs.__contains__('cardDetails'):
            raise serializers.ValidationError('cardDetails is required')
        if len(password) < 8:
            raise serializers.ValidationError('Password is too short, minimum length is 8')
        try:
            validate_email(email)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(f"bad email, details: {e}")
        return attrs

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
    class Meta:
        model = Seller
        fields = ('shopEmail', 'shopName', 'location')

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user_obj = self.context['request'].user
        seller = Seller.objects.create(user=user_obj,
                                       shopName=validated_data['shopName'],
                                       shopEmail=validated_data['shopEmail'],
                                       location=validated_data['location'])
        user_obj.is_seller = True
        user_obj.save()
        return seller

    def __delete__(self, instance):
        print(instance)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSimplestSerializer(read_only=True)
    products = ProductSimplestSerializer(read_only=True, many=True)
    img = serializers.ImageField

    class Meta:
        model = Profile
        fields = ['user', 'products', 'img']
