from rest_framework import viewsets
from .serializers import IndustrySerializer, LocationSerializer, CompanySerializer, PostJobSerializer, AvailableJobsSerializer
from .models import Industry, Location, Company, Job
from .permissions import IsAdminOrEmployer, IsEmployer, IsLocationOwner, IsCompanyOwner, IsJobOwner
from .throttles import CustomUserThrottle
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator

# Create your views here.
class IndustryViewset(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAdminOrEmployer]
    # For general keyword search
    search_fields = ['name', 'slug', 'description']


class LocationViewset(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsEmployer, IsLocationOwner]
    # For general keyword search
    search_fields = ['country', 'city', 'region', 'is_remote']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Location.objects.none()
        
        # Filter by created_by - only show user's own locations
        return Location.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set created_by
        serializer.save(created_by=self.request.user)


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsEmployer, IsCompanyOwner]
    # For general keyword search
    search_fields = ['name', 'slug', 'industry', 'location__country', 
                     'location__region', 'location__city', 'description', 
                     'website_url']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Company.objects.none()
        
        # Filter by created_by - only show user's own companies
        return Company.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set created_by
        # Permission class already checks for location requirement
        serializer.save(created_by=self.request.user)


class PostJobViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = PostJobSerializer
    permission_classes = [IsEmployer, IsJobOwner]
    throttle_classes = [CustomUserThrottle]
    # For general keyword searh
    search_fields = ['title', 'slug', 'industry__name', 'location__country', 
                     'location__region', 'description', 'experience_level', 
                     'requirements', 'responsibilities', 'skills_required']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Job.objects.none()
        
        # Filter by posted_by - only show user's own jobs
        return Job.objects.filter(posted_by=self.request.user)
    
    def perform_create(self, serializer):
        company = serializer.validated_data.get("company")
        industry = company.industry
        locations = company.locations.all()  # get all locations
        # Save the job instance first
        job = serializer.save(
            posted_by=self.request.user, # Automatically set posted_by and industry
            industry=industry, # Automatically industry
            )
        # Assign locations AFTER saving
        job.location.set(locations)  # .set() works for ManyToMany


class AvailableJobsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = AvailableJobsSerializer
    # For general keyword sear
    search_fields = ['title', 'slug', 'industry__name', 'location__country', 
                     'location__region', 'description', 'experience_level', 
                     'requirements', 'responsibilities', 'skills_required']