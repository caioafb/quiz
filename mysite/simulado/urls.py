from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'simulado'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('simulado/<int:pk>/', views.SimuladoView.as_view(), name='simulado'),
    path('profile/', views.PerfilView.as_view(), name='perfil'),
    path('result/', views.SimuladoView.as_view(), name='resultado'),
    path('register/', views.NovoUsuarioView.as_view(), name='novo_usuario'),
    path('new_question/', views.NovaQuestaoView.as_view(), name='nova_questao'),
    path('new_theme/', views.NovoTemaView.as_view(), name='novo_tema'),
    path('new_simulado/',views.NovoSimuladoView.as_view(), name='novo_simulado'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]