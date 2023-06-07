from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from ManageUsers.models import CustomUser


class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=(
            "email",
            "first_name",
            "last_name",
            #"password"
        )
        
class EditCustomProfileForm(UserChangeForm):
    password = None
    class Meta:
        model=CustomUser
        fields=(
            "university",
            "address",
            "regiment",
        )

