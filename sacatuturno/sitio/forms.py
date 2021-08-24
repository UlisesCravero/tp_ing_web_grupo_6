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


    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Ya existe una cuenta con este email')



    def save(self, commit=True):     
        print("estas en el save")   
        user = super(formularioUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # Usuario no activo hasta que valide su email
            user.save()

        return user