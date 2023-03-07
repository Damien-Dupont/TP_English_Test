from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('game/', views.game, name='game'),
    path('play/', views.play, name='play'),
    path('end/', views.end, name='end'),
]
