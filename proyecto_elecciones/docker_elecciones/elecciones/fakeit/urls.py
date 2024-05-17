
from django.urls import path
from . import views
from .views import IndexView

app_name = "fakeit"
urlpatterns = [
    path("",IndexView.acceso_home, name="index"),
    path("formulario/", IndexView.registrar_persona, name="guardar_persona"),
]
