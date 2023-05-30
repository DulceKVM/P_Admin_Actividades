from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


from .models import Actividad, Asignacion, Comentario, RespuestaActividad


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k: "" for k in fields}


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': '¿Alguna Tarea?'}), required=True)

    class Meta:
        model = Post
        fields = ['content']


# ADMINISTRADOR DE TAREAS


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'archivo_adjunto', 'estado']


class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['usuario', 'actividad']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['usuario', 'actividad', 'comentario']


class CrearActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'archivo_adjunto', 'trabajadores']

    trabajadores = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Trabajadores'),
        widget=forms.CheckboxSelectMultiple
    )


class ActualizarActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'archivo_adjunto', 'estado', 'trabajadores']

    trabajadores = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Trabajadores'),
        widget=forms.CheckboxSelectMultiple
    )


class ResponderActividadForm(forms.ModelForm):
    class Meta:
        model = RespuestaActividad
        fields = ['actividad', 'usuario', 'comentario', 'archivo_adjunto', 'estado']

    estado = forms.ChoiceField(choices=RespuestaActividad.ESTADOS_CHOICES)
