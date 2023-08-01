from django.db import models
from django.contrib.auth.models import User
# Create your models here.

SUBMISSION_TYPES = (
    ('image', 'Image'),
    ('file', 'File'),
    ('link', 'Link'),
)