from django import forms
from django.contrib.auth.forms import UserCreationForm       #importamos formularios de django
from django.contrib.auth.models import User                  #importamos usarios de django


class formularioUser(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username', 
            'password1', 
            'password2', 
            'email', 
        ]