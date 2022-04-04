from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('quiz/<int:pk>/', views.QuizView.as_view(), name='quiz'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('result/', views.QuizView.as_view(), name='result'),
    path('register/', views.NewUserView.as_view(), name='new_user'),
    path('new_question/', views.NewQuestionView.as_view(), name='new_question'),
    path('new_theme/', views.NewThemeView.as_view(), name='new_theme'),
    path('new_quiz/',views.NewQuizView.as_view(), name='new_quiz'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
