from django.contrib import admin

from .models import Exercise, Type, MuscleGroup, SingleMuscle


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name']
    list_editable = ['name']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(SingleMuscle)
class SingleMuscleAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'muscle_group']
    list_editable = ['name', 'muscle_group']
    list_filter = ['muscle_group']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'description', 'type']
    list_filter = ['type', 'muscles']
    list_editable = ['name', 'description', 'type']
    prepopulated_fields = {"slug": ("name",)}

# @admin.register(Type)
# class TypeAdmin(admin.ModelAdmin):
#     list_display = ['slug', 'name']
#     list_editable = ['name']
#     prepopulated_fields = {"slug": ("name",)}