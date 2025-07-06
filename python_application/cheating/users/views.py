from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import User
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm
import os

def login(request):
    if request.method=="POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:popular_list'))
            
            # Добавление в форму подсказки пользователю
            form.add_error(None, "Неверный логин или пароль")
    else:   
        # Очистка формы
        form = UserLoginForm()
    return render(request, "users/login.html", {"form":form})

def registration(request):
    if request.method=="POST":
        form = UserRegistrationForm(data = request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f'{user.username} зарегистрирован')
            return HttpResponseRedirect(reverse("users:login"))
    else:
        form = UserRegistrationForm()
    return render(request, "users/registration.html", {"form":form})

@login_required
def profile(request):
    if request.method=="POST":
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль был изменен")
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)
    likes = request.user.favorites.all()
    return render(request, "users/profile.html", {"form": form, "exercises": likes})


def logout(request):
    auth.logout(request)
    return redirect(reverse("main:popular_list"))

def enter_email(request):
    return render(request, "users/enter_email.html")

def verify_password(request):
    to_email = request.POST.get("email")
    recieved_code = request.POST.get("code")
    if to_email:
        # Если email был введен
        try:
            usr = User.objects.get(email=to_email)
            code = str(random.randint(100000, 999999))
            # Сохранение отправляемого кода в сессии
            request.session['verify_code'] = code

            subject = 'Служба восстановления пароля Cheating'
            from_email = os.environ.get("EMAIL_HOST_USER")

            html_content = render_to_string('mail.html', {'code': code})
            text_content = f'Ваш код подтверждения: {code}'

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return render(request, "users/enter_code.html", {"user_to_change": usr})
        except User.DoesNotExist:
            # Неверная почта
            return render(request, "users/enter_email.html", {"error":"Пользователя с такой почтой не существует", "email":to_email})
        
    usr = User.objects.get(id=request.POST.get("user_to_change"))
    
    if recieved_code==request.session['verify_code']:
        # Код введен правильно
        return render(request, "users/change_password.html", {"user_to_change": usr})
    # Код введен неправильно
    return render(request, "users/enter_code.html", {"user_to_change":usr, "error":"Неверный код"})


def change_password(request):
    usr = User.objects.get(id=request.POST.get("user_to_change"))
    if request.method == "POST":
        form = SetPasswordForm(user=usr, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("users:login"))
    else:
        form = SetPasswordForm(user=usr)

    return render(request,
                  "users/change_password.html",
                  {"form": form, "user_to_change": usr})