from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Actividad, Asignacion, Comentario
from .forms import ActividadForm, AsignacionForm, ComentarioForm

# Create your views here.


def feed(request):
    posts = Post.objects.all()

    context = {'posts': posts}
    return render(request, 'social/feed.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado exitosamente')
            return redirect('feed')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'social/register.html', context)


def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'Tareas Notificadas')
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social/post.html', {'form': form})


def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'social/profile.html', {'user': user, 'posts': posts})

# ADMINISTRADOR DE ACTIVIDADES


@login_required
def actividad_list_view(request):
    actividades = Actividad.objects.all()
    context = {
        'actividades': actividades
    }
    return render(request, 'social/list.html', context)


@login_required
def actividad_detail_view(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    asignaciones = Asignacion.objects.filter(actividad=actividad)
    comentarios = Comentario.objects.filter(actividad=actividad)
    if request.method == 'POST':
        if 'completado' in request.POST:
            actividad.completada = True
            actividad.save()
        elif 'no_completado' in request.POST:
            actividad.completada = False
            actividad.save()
    context = {
        'actividad': actividad,
        'asignaciones': asignaciones,
        'comentarios': comentarios
    }
    return render(request, 'social/detail.html', context)


@login_required
def actividad_create_view(request):
    form = ActividadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        actividad = form.save(commit=False)
        actividad.creador = request.user
        actividad.save()
        return redirect('actividad-detail', actividad_id=actividad.id)
    actividades = Actividad.objects.all()
    context = {
        'form': form,
        'actividades': actividades
    }
    return render(request, 'social/create.html', context)


@login_required
def asignacion_create_view(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    form = AsignacionForm(request.POST or None)
    if form.is_valid():
        asignacion = form.save(commit=False)
        asignacion.actividad = actividad
        asignacion.save()
        return redirect('actividad-detail', actividad_id=actividad.id)
    context = {
        'actividad': actividad,
        'form': form,
    }
    return render(request, 'social/asignacion_create.html', context)


#@login_required
#def asignacion_create_view(request, actividad_id):
#    actividad = get_object_or_404(Actividad, id=actividad_id)
#    asignacion_actual = actividad.asignaciones.first()
#    form = AsignacionForm(request.POST or None)
#    if form.is_valid():
#        asignacion = form.save(commit=False)
#        asignacion.actividad = actividad
#        asignacion.save()
#        return redirect('actividad-detail', actividad_id=actividad.id)
#    actividades = Actividad.objects.all()
#    context = {
#        'actividad': actividad,
#        'form': form,
#        'actividades': actividades,
#        'asignado_a': asignacion_actual.usuario.username if asignacion_actual else None,
#    }
#    return render(request, 'social/asignacion_create.html', context)


@login_required
def comentario_create_view(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    form = ComentarioForm(request.POST or None)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.actividad = actividad
        comentario.usuario = request.user
        comentario.save()
        return redirect('actividad-detail', actividad_id=actividad.id)
    context = {
        'actividad': actividad,
        'form': form
    }
    return render(request, 'social/comentario_create.html', context)