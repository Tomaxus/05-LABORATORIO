from django.urls import path

from . import views

urlpatterns = [
    path("csrf/", views.csrf, name="auth-csrf"),
    path("registro/", views.registro, name="auth-registro"),
    path("login/", views.login_view, name="auth-login"),
    path("logout/", views.logout_view, name="auth-logout"),
    path("yo/", views.yo, name="auth-yo"),
]
