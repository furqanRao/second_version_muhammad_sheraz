from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from datetime import date


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'age', 'gender', 'country', 'city']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'cities']


class ProductDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductData
        fields = '__all__'

    def create(self, validated_data):
        return ProductData.objects.create(**validated_data)
