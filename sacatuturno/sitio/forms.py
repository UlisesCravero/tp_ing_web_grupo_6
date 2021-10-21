
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm       #importamos formularios de django
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django.forms import widgets                  #importamos usarios de django
from .models import *

class formularioUser(UserCreationForm):
    email = forms.EmailField(label="Email")
    nombre = forms.CharField(label="Nombre", max_length=50)
    apellido = forms.CharField(label="Apellido", max_length=50)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = [
            'username', 
            'nombre',
            'apellido',
            'password1', 
            'password2', 
            'email', 
        ]


    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Ya existe una cuenta con este email')



    def save(self, commit=True):      
        user = super(formularioUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        if commit:
            user.is_active = False # Usuario no activo hasta que valide su email
            user.save()

        return user

class formularioProfesional(forms.ModelForm):
    class Meta:
        model = ServicioPrestado
        fields = ['nombre', 'descripcion', 'categoria', 'subcategoria', 'diasAtencion', 'duracionTurno', 'ciudad']
        widgets = {
            'categoria' : forms.Select(attrs={'onchange': 'mostrarSubcategorias()'},),
            'diasAtencion': forms.SelectMultiple 
        }

    def init(self, args, **kwargs):
        super().init(args, **kwargs)

        self.fields["categoria"].required = False
      


class formularioTurno(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'placeholder': 'Select a datetime',
                    'type': 'datetime-local'
                    }),
            'fecha_fin': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'placeholder': 'Select a datetime',
                    'type': 'datetime-local'
                    }),   
        }
