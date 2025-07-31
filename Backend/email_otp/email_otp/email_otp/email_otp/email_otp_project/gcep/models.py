from django.db import models
from django.utils import timezone

# Create your models here.

class ContactForm(models.Model):
    # Name fields (First and Last name)
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    
    # Institute field
    institute = models.CharField(max_length=200, verbose_name="Institute")
    
    # Designation field (optional)
    designation = models.CharField(max_length=200, blank=True, null=True, verbose_name="Designation (if agency)")
    
    # Email field
    email = models.EmailField(verbose_name="Email")
    
    # Phone field (optional)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    
    # Job Title field (optional)
    job_title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Job Title")
    
    # Message field
    message = models.TextField(verbose_name="Message")
    
    # Timestamp
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    
    class Meta:
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
