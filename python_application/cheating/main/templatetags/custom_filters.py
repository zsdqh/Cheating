from django import template
from users.models import User
from main.models import Exercise
register = template.Library()

@register.filter
def get_item(dict_obj, key):
    return dict_obj.get(key, [])

@register.filter
def is_liked(exercise:Exercise, user:User):
    if user.is_anonymous:
        return False
    return user.favorites.contains(exercise)