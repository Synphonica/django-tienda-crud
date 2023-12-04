from django import forms
from .models import Libro, Perfil, Comentario
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser  
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        help_text='Required. Enter a valid email address.'
    )
    imagen = forms.ImageField(required=False)  # Campo para subir imagen
    is_staff = forms.BooleanField(required=False, label='Administrador')  # Nuevo campo para seleccionar si el usuario es administrador

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'imagen', 'is_staff']  # Incluye 'is_staff' en los campos 

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('El nombre de usuario ya existe.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    correo = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'correo']


class ProfileUpdateForm(forms.ModelForm):
    usuario = forms.CharField(max_length=255, required=False)
    correo = forms.EmailField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Perfil
        fields = ['usuario', 'correo', 'descripcion', 'foto_de_perfil']

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )

class CambiarContrasenaForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'}),
    )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
    )

class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text='150 caracteres como máximo.', required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    foto_de_perfil = forms.ImageField(required=False)

    class Meta:
        model = Perfil
        fields = ['username', 'descripcion', 'foto_de_perfil']
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'puntuacion']