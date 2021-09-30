from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('crear-cuenta/', crearcuenta, name = 'crearcuenta'),
    path('login/', login, name = 'login'),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name= 'logout'),
    path('perfil/<int:id>/', login_required(perfil), name='perfil'),
    path('accounts/confirm/<str:activation_key>', register_confirm, name="activation"),
    path('categorias/', categorias, name='categorias'),
    path('paginaprivada/', login_required(paginaprivada), name='paginaprivada'),
    path('categorias/subcategoria/<int:id>/', subcategoria, name = 'subcategoria'), 
    path('servicios/<int:id_subcategoria>/', servicios, name = 'servicios'),    
    path('registrarservicio/', login_required(registrarservicio), name = 'registrarservicio'),
    path('traerSubcategorias/<int:id_categoria>/', login_required(traerSubcategorias), name = 'traerSubcategorias'),
    path('delete_servicio/<int:id>/<int:id_user>/', login_required(eliminar_servicio), name='eliminar_servicio'),
    path('edit_servicio/<int:servicio_id>/<int:id_user>/', login_required(editar_servicio), name='editar_servicio'),
    path('turno/<int:servicio_id>/<int:id_user>/', login_required(pedir_turno), name='pedir_turno'),
]