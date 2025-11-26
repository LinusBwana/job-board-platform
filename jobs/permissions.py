from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    # Only admin users can access
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated 
                and (request.user.is_staff or request.user.role == 'admin'))
    

class IsAdminOrEmployer(BasePermission):
    def has_permission(self, request, view):
        if (not request.user or not request.user.is_authenticated):
            return False

        if request.method == 'GET' and request.user.role == 'employer':
            return True
        
        if (request.user.is_staff or request.user.role == 'admin'):
            return True
        
        return False
   
    
class IsEmployer(BasePermission):
    # Only authenticated users with 'employer' role can access
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'employer') 


class IsLocationOwner(BasePermission):
    """
    Only employers can create locations
    Users can only access locations they created
    """
    def has_object_permission(self, request, view, obj):
        # Check if user created this location
        return obj.created_by == request.user
    

class IsCompanyOwner(BasePermission):
    """
    Only employers can create companies
    Users can only access companies they created
    Must have created at least one location to create a company
    """
    def has_permission(self, request, view):
        # For POST (create), check if user has created locations
        if request.method == 'POST':
            from .models import Location
            has_locations = Location.objects.filter(created_by=request.user).exists()
            if not has_locations:
                return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        # Check if the user created this company
        return obj.created_by == request.user
    

class IsJobOwner(BasePermission):
    """
    Only employers can create jobs
    Users can only access jobs they posted
    Must own a company to post a job
    """
    def has_permission(self, request, view):  
        # For POST (create), check if user owns a company
        if request.method == 'POST':
            from .models import Company
            owns_company = Company.objects.filter(created_by=request.user).exists()
            if not owns_company:
                return False
            
        return True
    
    def has_object_permission(self, request, view, obj):
        # Check if the user posted this job
        return obj.posted_by == request.user