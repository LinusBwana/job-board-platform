from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewset, MyApplicationViewset, JobApplicationsViewset

router = DefaultRouter()
router.register(r'applications', ApplicationViewset, basename='applications')
router.register(r'my-applications', MyApplicationViewset, basename='my-applications')
router.register(r'job-applications', JobApplicationsViewset, basename='job-applications')

urlpatterns = [
    path('api/', include(router.urls)),
]