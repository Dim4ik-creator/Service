from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from .models import CustomUser, Task

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('leader', 'Тимлид'),
        ('member', 'Участник'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'role-dropdown'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')


        if username:
            user = CustomUser.objects.filter(username=username).first()
            if user and user.is_blocked:
                raise forms.ValidationError("Ваш аккаунт заблокирован администратором.")

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'role', 'password')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'creator']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
            'status': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
        }
