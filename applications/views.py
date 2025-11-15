from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ApplicationSerializer, ApplicationHistorySerializer, EmployerApplicationSerializer
from .models import Application

# Create your views here.
class ApplicationViewset(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

# For Job Seekers - "My Applications"
class MyApplicationViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicationHistorySerializer
    def get_queryset(self):
        return Application.objects.all(
            # applicant=self.request.user
        ).select_related('job', 'job__company').order_by('-applied_on')


# For Employers - "Applications to My Jobs"
class JobApplicationsViewset(viewsets.ModelViewSet):
    serializer_class = EmployerApplicationSerializer
    http_method_names = ['get', 'put']
    def get_queryset(self):
        return Application.objects.all(
            # job__posted_by=self.request.user
        ).select_related('job', 'applicant').order_by('-applied_on')
