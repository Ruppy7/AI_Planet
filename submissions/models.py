from django.db import models
from django.contrib.auth.models import User, AbstractUser
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
