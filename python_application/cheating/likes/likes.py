from main.models import Exercise
from users.models import User

class Likes:
    # Класс для работы "сердечка"
    def __init__(self, request):
        self.user: User = request.user
        self.likes = self.user.favorites

    def clicked(self, exercise: Exercise):
        # Добавление\удаление упражнения в понравившиеся при клике
        if self.likes.filter(id=exercise.id).exists():
            self.likes.remove(exercise)
            return "remove"
        else:
            self.likes.add(exercise)
            return "add"