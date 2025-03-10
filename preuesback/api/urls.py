from django.urls import path
from . import views

urlpatterns = [
    path("Usuarios/", views.UsuarioListCreate.as_view(), name="Usuario-list-create"),
    path("signup/", views.CreateUsuarioApiView.as_view(), name = "Create user"),
]