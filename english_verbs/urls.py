from django.urls import path
from django.contrib import admin

from django.views.defaults import page_not_found
from django.views.defaults import server_error

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('game/', views.game, name='game'),
    path('play/', views.play, name='play'),
    path('end/', views.end, name='end'),
    
    path('admin/', admin.site.urls),
    path('404/', page_not_found),
    path('500/', server_error)]
