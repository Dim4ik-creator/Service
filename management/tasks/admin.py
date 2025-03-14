from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Поля для отображения в списке пользователей
    list_display = ('username', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_blocked')  # Добавляем фильтр по блокировке
    # Поля, доступные для редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('name', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля при добавлении пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('username', 'name')
    ordering = ('username',)


# Регистрируем кастомную модель пользователя
admin.site.register(CustomUser, CustomUserAdmin)
