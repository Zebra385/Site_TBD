from django.contrib import admin
from .models import  CustomUser

from django.contrib.auth.admin import UserAdmin 

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin): 
    pass