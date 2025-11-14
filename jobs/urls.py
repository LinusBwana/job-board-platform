from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewset, LocationViewset, CompanyViewset, JobViewset

router = DefaultRouter()
router.register(r'categories', CategoryViewset, basename='category')
router.register(r'locations', LocationViewset, basename='locations')
router.register(r'companies', CompanyViewset, basename='companies')
router.register(r'jobs', JobViewset, basename='jobs')

urlpatterns = [
    path('api/', include(router.urls)),
]