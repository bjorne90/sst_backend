from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # This is for the Browsable API
    path('api/', include('scheduling.urls')),  # Assuming your scheduling app's APIs are at the 'api/' path
    path('api/', include('authentication.urls')),  # This is for the Authentication APIs
    path('api/', include('profiles.urls')),  # This is for the Profiles APIs
    path('api/', include('booking.urls')),
    path('', views.home, name='home'),
]
