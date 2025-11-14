from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import MinValueValidator

# Create your models here.
class User(AbstractUser):
    role_choices = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True, 
        editable=False)
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=150, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        choices=role_choices, 
        max_length=50, 
        null=True,
        blank=True, 
        default='job_seeker')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True)
    resume = models.FileField(
        upload_to='resumes/', 
        blank=True, 
        null=True)
    linkedIn_url = models.URLField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    experience_years = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []