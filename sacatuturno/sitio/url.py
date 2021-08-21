from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('crear-cuenta/', crearcuenta, name = 'crearcuenta'),
    path('login/', LoginView.as_view(template_name='login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name= 'logout'),
    path('perfil/', login_required(perfil), name='perfil')
]