from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.feed, name='feed'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
    path('post/', views.post, name='post'),
    # ADMINISTRADOR DE TAREAS
    path('actividad/', views.actividad_list_view, name='actividad-list'),
    path('actividad/<int:actividad_id>/', views.actividad_detail_view, name='actividad-detail'),
    path('actividad/create/', views.actividad_create_view, name='actividad-create'),
    #path('actividad/<int:actividad_id>/asignacion/create/', views.asignacion_create_view, name='asignacion-create'),
    path('actividad/<int:actividad_id>/asignacion/create/', views.asignacion_create_view, name='asignacion-create'),
    path('actividad/<int:actividad_id>/comentario/create/', views.comentario_create_view, name='comentario-create'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)