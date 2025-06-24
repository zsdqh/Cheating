from django.urls import path
from . import views

app_name='main'

urlpatterns = [
    path('', views.popular_list, name='popular_list'),
    path('exercise/<slug:exercise_slug>/', views.exercise_detail, name='exercise_detail'),
    path('muscle/<slug:muscle_slug>/', views.exercise_list, name='exercises_by_muscle'),
    path('filtered', view=views.filtered_list, name="filtered_list")
]
