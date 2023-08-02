from django.contrib import admin
from .models import CustomUser, Hackathon, Submission, Enrollment

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Hackathon)
admin.site.register(Enrollment)
admin.site.register(Submission)