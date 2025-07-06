import random

from django.db import models
from django.urls import reverse


class MuscleGroup(models.Model):
    # Группа мышц, объединяющая несколько мышц в одну группу
    name = models.CharField(max_length=50, unique=True, verbose_name="Имя")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Ссылочное имя")

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Группа мышц'
        verbose_name_plural = 'Группы мышц'

    def __str__(self):
        return self.name


class Type(models.Model):
    # Тип упражнения, может быть Основное, Изолирующее, Разминочное
    name = models.CharField(max_length=50, unique=True, verbose_name="Имя")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Ссылочное имя")

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class SingleMuscle(models.Model):
    # Одна мышца, которая принадлежит какой-либо группе
    name = models.CharField(max_length=50, unique=True, verbose_name="Имя")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Ссылочное имя")
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.CASCADE,
        related_name='muscles',
        verbose_name="Группа мышц"
    )

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Мышца'
        verbose_name_plural = 'Мышцы'

    def get_absolute_url(self):
        return reverse("main:exercises_by_muscle", args=[self.slug])

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Имя")
    image = models.ImageField(blank=True, upload_to='exercises', verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание")
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name="Тип упражнения"
    )
    muscles = models.ManyToManyField(SingleMuscle, verbose_name="Задействованные мышцы")
    slug = models.SlugField(unique=True, verbose_name="Ссылочное имя")
    video_link = models.URLField(blank=True, verbose_name="Ссылка на видео")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name'])
        ]
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:exercise_detail", args=[self.slug])
