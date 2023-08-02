from django.urls import path
from . import views
from .views import links, knowledge_base

app_name = 'profiles'

urlpatterns = [
    path('detail/', views.profile_detail, name='profile_detail'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('work_shifts/', views.work_shifts, name='work_shifts'),
    path('links/', links, name='links'),
    path('employees/', views.employees, name='employees'),
    path('detail/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('admin/employee_profiles/', views.admin_view_profiles, name='admin_view_profiles'),
    path('knowledgebase/', knowledge_base, name='knowledgebase'),
]
