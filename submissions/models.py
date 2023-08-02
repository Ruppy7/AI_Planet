from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('enrol_hackathon', 'Enrol_hackathon'),
        ('list_hackathon', 'List_hackathon'),
    )
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)

class Hackathon(models.Model):
    SUBMISSION_TYPES = [
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    bg_img = models.ImageField(upload_to='hackathon_bg/')
    hackathon_img = models.ImageField(upload_to='hackathon_images/')
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPES)
    start = models.DateTimeField()
    end = models.DateTimeField()
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.hackathon.title}"


class Submission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    summary = models.TextField()

    # Submission fields based on hackathon_submission_type
    submission_file = models.FileField(upload_to='submissions/files/', blank=True, null=True)
    submission_image = models.ImageField(upload_to='submissions/images/', blank=True, null=True)
    submission_link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        hackathon_submission_type = self.hackathon.submission_type

        if hackathon_submission_type == 'image':
            if self.submission_file or self.submission_link:
                raise ValidationError("Invalid submission data for the hackathon type.")
        elif hackathon_submission_type == 'file':
            if self.submission_image or self.submission_link:
                raise ValidationError("Invalid submission data for the hackathon type.")
        elif hackathon_submission_type == 'link':
            if self.submission_file or self.submission_image:
                raise ValidationError("Invalid submission data for the hackathon type.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.name}"