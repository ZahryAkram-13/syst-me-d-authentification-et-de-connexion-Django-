from django.urls import path
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    
    path("", views.home, name="home"),

    path("signup", views.Signup.as_view(), name = "signup"),
    path("login", views.Login.as_view(), name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("account", views.account, name = "account"),
    path("update_profil", views.update_profil, name = "update_profil")

]


