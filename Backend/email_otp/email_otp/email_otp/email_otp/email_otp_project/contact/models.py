from django.db import models

EDUCATION_CHOICES = [
    ('B.Sc', 'B.Sc'),
    ('M.Sc', 'M.Sc'),
    ('PhD', 'PhD'),
    # Add more as needed
]

STREAM_CHOICES = [
    ('Computer Science', 'Computer Science'),
    ('Mathematics', 'Mathematics'),
    ('Physics', 'Physics'),
    # Add more as needed
]

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    education_qualification = models.CharField(max_length=100, choices=EDUCATION_CHOICES)
    stream = models.CharField(max_length=100, choices=STREAM_CHOICES)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}" 