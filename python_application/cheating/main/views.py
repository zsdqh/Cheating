import random
from django.shortcuts import render, get_object_or_404
from .models import Exercise, SingleMuscle, MuscleGroup
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

index_default:dict = None # Информация, передаваемая в index.html всегда
ITEMS_ON_PAGE = 6 # Количество карточек упражнений на странице при пагинации

def get_default():
    global index_default
    if not index_default:
        create_default()
    return index_default

def create_default():
    global index_default
    index_default = {
                 "muscle_groups": list(MuscleGroup.objects.all()), # Все группы мышц для фильтрации
                 "muscles": {group.slug: [muscle for muscle in SingleMuscle.objects.filter(muscle_group=group)] for
                             group in MuscleGroup.objects.all()}, # Все мышцы для фильтрации
                 "excluded": {"Разогрев", "Растяжка"}, # Исключенные "мышцы" для правильного отображения в основных и изоляционных упражнениях
                 "checked":{}
                 }

def popular_list(request):
    exercises = list(Exercise.objects.filter())
    # random.shuffle(exercises) # Если нужно выводить упражнения на главной странице в случайном порядке

    page = request.GET.get("page", 1)
    paginator = Paginator(exercises, ITEMS_ON_PAGE)
    current_page = paginator.page(int(page))
    return render(request, "main/index/index.html", {'exercises': current_page, **get_default()})


def exercise_detail(request, exercise_slug):
    exercise = get_object_or_404(Exercise, slug=exercise_slug)
    return render(request, "main/exercise/detail.html", {'exercise': exercise})


def exercise_list(request, muscle_slug=None):
    muscle = None
    exercises = Exercise.objects.filter()

    if muscle_slug:
        # Обработка нажатия на серый прямоугольник(передачу мышцы в запрос)
        try:
            muscle = SingleMuscle.objects.get(slug=muscle_slug)
        except SingleMuscle.DoesNotExist:
            return render(request, 'main/index/index.html', {'exercises': [], **get_default()})
        exercises = exercises.filter(muscles__in=[muscle])

    if len(exercises) > 1:
        # Загрузить index.html с отфильтрованными упражнениями
        page = request.GET.get("page", 1)
        paginator = Paginator(exercises, ITEMS_ON_PAGE)
        current_page = paginator.page(int(page))
        return render(request, 'main/index/index.html', {'exercises': current_page, 'muscle': muscle, **get_default()})
    elif len(exercises) == 1:
        # Если нашлось только одно упражнение, то открыть его страницу
        return render(request, 'main/exercise/detail.html', {'exercise': exercises[0]})


def filtered_list(request):
    if request.method == 'POST':
        # Для создания пагинации храним результат запроса в сессии и обновляем его при каждом новом POST запросе
        request.session['filter_params'] = {
            'warmup': request.POST.getlist("warmup"),
            'isolating_muscle': request.POST.getlist("isolating_muscle"),
            'main_muscle': request.POST.getlist("main_muscle"),
            'user_input': request.POST.get("user_input", "")
        }
    # Восстанавливаем параметры из сессии при пагинации
    filter_params = request.session.get('filter_params', {})

    warmup = set(filter_params.get("warmup", []))
    isolating_muscles = set(filter_params.get("isolating_muscle", []))
    main_muscles = set(filter_params.get("main_muscle", []))
    user_input = filter_params.get("user_input", "")
    checked = {}

    def filter_exercises_by_type(type_slug, typed_muscles)->list:
        # Фильтрация упражнений по типу
        return list(exercises.filter(type__slug=type_slug, muscles__slug__in=typed_muscles).distinct())
    
    exercises = Exercise.objects.filter(name__icontains=user_input)

    if warmup or isolating_muscles or main_muscles:
        #Если задана фильтрация по мышцам
        warmup_exercises = list(exercises.filter(type__slug="razminochnoe").filter(
                Q(muscles__slug__in=warmup) |
                Q(muscles__muscle_group__slug__in=warmup)
            ).distinct()
        )
        isolating_exercises = filter_exercises_by_type("izoliruyushee", isolating_muscles)
        main_exercises = filter_exercises_by_type("osnovnoe", main_muscles)

        # Объединение подходящих упражнений и удаление повторений
        exercises = set(warmup_exercises+isolating_exercises+main_exercises)

        # Сохранение параметров выбора между страницами
        checked = {"warmup": warmup, "isolating": isolating_muscles, "main":main_muscles}

    if len(exercises)==1:
        # Если найдено только одно упражнение, то загрузить его страницу
        return redirect(reverse('main:exercise_detail', args=[exercises.pop().slug]))
    
    page = request.GET.get("page", 1)  
    paginator = Paginator(list(exercises), ITEMS_ON_PAGE)
    current_page = paginator.page(int(page))
    return render(request, 'main/index/index.html', {"exercises":current_page,  **get_default(), "checked":checked, "text":user_input})
