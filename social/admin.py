from django.contrib import admin
from .models import Post, Profile, Actividad, Asignacion, Comentario, RespuestaActividad

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
# ADMINISTRADOR DE TAREAS
admin.site.register(Actividad)
admin.site.register(Asignacion)
admin.site.register(Comentario)
admin.site.register(RespuestaActividad)