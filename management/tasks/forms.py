from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_blocked:
                raise forms.ValidationError("Ваш аккаунт заблокирован администратором.")

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name')
