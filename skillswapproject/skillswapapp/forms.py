from django import forms
from .models import Skill
from django.contrib.auth.models import User
from .models import UserProfile

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["type", "title", "description", "category", "availability", "location"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
