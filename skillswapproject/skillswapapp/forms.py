from django import forms
from .models import Skill
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ['title', 'description', 'category', 'availability', 'location']
       
class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    fullname = forms.CharField(label='Full Name', max_length=150, required=True)

    class Meta:
        model = User
        fields = ['username', 'fullname', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        full = self.cleaned_data['fullname'].strip().split(' ', 1)
        user.first_name = full[0]
        user.last_name = full[1] if len(full) > 1 else ''
        if commit:
            user.save()
        return user
