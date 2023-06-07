from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from ManageUsers.models import CustomUser

# Define an inline admin descriptor for CustomUser model
# which acts a bit like a singleton
