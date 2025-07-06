from django.urls import path
from . import views

app_name='likes'

urlpatterns = [
    path('favorite/<slug:exercise_slug>/', views.toggle_favorite, name='toggle_favorite'),
]
