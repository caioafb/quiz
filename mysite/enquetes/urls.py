from django.urls import path
from . import views

app_name = "enquetes"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('cadastro', views.CadastroView.as_view(), name="cadastro"),
    path('<int:pk>/', views.DetalhesView.as_view(), name="detalhes"),
    path('<int:pk>/votacao', views.VotacaoView.as_view(), name="votacao"),
    path('<int:pk>/resultado', views.ResultadoView.as_view(), name="resultado"),
    #path('', views.index, name="index"),
    #path('<int:id_enquete>/', views.detalhes, name="detalhes"),
    #path('<int:id_enquete>/votacao', views.votacao, name="votacao"),
    #path('<int:id_enquete>/resultado', views.resultado, name="resultado"),
]