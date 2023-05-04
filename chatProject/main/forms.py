from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from .models import Profile, Messages

"""
    Если у тебя будет много форм лучше создать отдельную папку forms
    и раскидать их по файлам.
"""

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class MessageForm(ModelForm):
    class Meta:
        model = Messages
        widgets = {
            'text': Textarea(),
        }
        fields = ['text']
