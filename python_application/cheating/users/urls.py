from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("verify_password/", views.verify_password, name="verify_password"),
    path("change_password/", views.change_password, name="change_password"),
    path("enter_email/", views.enter_email, name="enter_email")
]
