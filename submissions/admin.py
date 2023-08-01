from django.contrib import admin
from .models import CustomUser, Hackathon
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Hackathon)