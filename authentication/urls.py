from django.urls import path
from .views import UserCreate, UserLogin

app_name = 'authentication'

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    # path('login2/', views.user_login2, name='login2'),  # If you don't need this anymore, you can comment or remove it
    # path('logout/', views.user_logout, name='logout'),  # Since logout is usually handled client-side with JWT, you might not need this
]
