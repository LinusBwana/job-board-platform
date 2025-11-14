from django.db import models
import uuid
import jobs
from jobs.models import Job
from django.conf import settings

# Create your models here.
class Application(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='jobs')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        choices=status_choices,
        max_length=50,
        default='pending',
    )
    cover_letter = models.TextField()
    resume = models.FileField(
        upload_to='application_documents/settings.AUTH_USER_MODEL/',
        blank=False, 
        null=False,
    )
    additional_documents = models.FileField(
        upload_to='application_documents/settings.AUTH_USER_MODEL/',
        blank=True, 
        null=True,
    )
    experience_years = models.PositiveIntegerField(default=0)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, 
                                          blank=False, null=False)
    availabilty_date = models.DateField()
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL, 
                                    null=True, related_name='reviewed_applications')
    reviewed_at = models.DateTimeField(blank=True, null=True,
                                       help_text="Date and time when the application was reviewed")
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ['-applied_on']
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['applicant']),
            models.Index(fields=['status']),
            models.Index(fields=['applied_on']),
        ]

    def __str__(self):
        return f"{self.job.category.name} applied on {self.applied_on}. Stage: {self.status})"
    

class ApplicationStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          editable=False, unique=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Application Status History"
        verbose_name_plural = "Application Status Histories"
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.application.applicant} - {self.status} applied on {self.application.applied_on}"