from django.contrib import admin
from .models import Industry, Location, Company, Job

class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at', 'updated_at']
admin.site.register(Industry, IndustryAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ['country', 'city', 'region', 'is_remote']
admin.site.register(Location, LocationAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name','industry',  'is_verified', 'website_url', 'created_at']
admin.site.register(Company, CompanyAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'job_type', 'is_active', 'posted_on']
admin.site.register(Job, JobAdmin)