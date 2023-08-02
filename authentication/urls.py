from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('login2/', views.user_login2, name='login2'),
    path('logout/', views.user_logout, name='logout'),
]
