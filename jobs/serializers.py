from rest_framework import serializers
from .models import Category, Location, Company, Job

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'is_active', 'created_at', 'updated_at']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'country', 'city', 'region', 'is_remote', 'created_at']
        read_only_fields = ['id', 'created_at']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'industry', 'is_verified', 'created_at', 'updated_at']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'posted_on', 'updated_on']