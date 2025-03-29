from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField("ФИО", max_length=100)
    is_blocked = models.BooleanField(default=False)  # Поле блокировки

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
