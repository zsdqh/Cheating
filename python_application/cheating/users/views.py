from django.shortcuts import render

def login(request):
    return render(request, "users/login.html")

def registration(request):
    return render(request, "users/registration.html")

def profile(request):
    return render(request, "users/profile.html")

def logout(request):
    pass
