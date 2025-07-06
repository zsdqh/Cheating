from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Exercise

class User(AbstractUser):
    # Расширение стандартного User для возможности хранения аватара и любимых упражнений
    image = models.ImageField(upload_to="users_image", blank=True, null=True, verbose_name="Аватар")
    favorites = models.ManyToManyField(Exercise, verbose_name="Любимые", blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = "user"

    def __str__(self):
        return self.username