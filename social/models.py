from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='GreenTech.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.content}'

# ADMINISTRADOR DE ACTIVIDADES


class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    archivo_adjunto = models.FileField(upload_to='archivos/')
    estado = models.BooleanField(default=False)


class Asignacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)


class RespuestaActividad(models.Model):
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('terminado', 'Terminado'),
    ]
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='respuestas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas')
    comentario = models.TextField()
    archivo_adjunto = models.FileField(upload_to='archivos_adjuntos/', blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADOS_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
