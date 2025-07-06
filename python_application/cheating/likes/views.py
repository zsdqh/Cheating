from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from main.models import Exercise
from .likes import Likes

@login_required
@require_POST
def toggle_favorite(request, exercise_slug):
    exercise = get_object_or_404(Exercise, slug=exercise_slug)
    current = Likes(request)
    action = current.clicked(exercise)
    return JsonResponse({"status": action})
