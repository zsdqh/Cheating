from django.conf import settings
from main.models import Exercise

class Likes:
    def __init__(self, request):
        self.session = request.session
        likes = self.session.get(settings.LIKES_SESSION_ID)
        if not likes:
            likes = self.session[settings.LIKES_SESSION_ID] = set()
        self.likes = likes

    def clicked(self, exercise: Exercise):
        exercise_id = str(exercise.id)
        if exercise_id not in self.likes:
            self.likes.add(exercise_id)
        else:
            self.likes.remove(exercise_id)
        self.save
    
    def save(self):
        self.session.modified = True
    
    def __iter__(self):
        exercises = Exercise.objects.filter(id__in=self.likes)
        for exercise in exercises:
            yield exercise
    
    def __len__(self):
        return len(self.likes)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]