from enum import unique

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    name = models.CharField("ФИО", max_length=100)
    is_blocked = models.BooleanField(default=False)  # Поле блокировки
    ROLE_CHOICES = [
        ('leader', 'Тимлид'),
        ('member', 'Участник'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    is_leader = models.BooleanField(default=False, verbose_name="Тимлид")  # Галочка в админке

    def save(self, *args, **kwargs):
        """Автоматически устанавливает is_leader в зависимости от роли."""
        self.is_leader = self.role == 'leader'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'


class Task(models.Model):
    STATUS_CHOICES = [
        ('backlog', 'Беклог'),
        ('inprogress', 'В процессе'),
        ('done', 'Выполнено'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    leader = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="team_leader")
    members = models.ManyToManyField(CustomUser, related_name="teams", blank=True)
    invite_code = models.CharField(max_length=10, unique=True, blank=True)

    def generate_invite_code(self):
        self.invite_code = str(uuid.uuid4())[:10]
        self.save()

    def __str__(self):
        return self.name
