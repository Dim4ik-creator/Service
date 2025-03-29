from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Task
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
        fields = ('username', 'name')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
            'status': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),

        }
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status','creator']
