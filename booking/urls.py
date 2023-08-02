from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('list/', views.booking_list, name='booking_list'),
    path('book/', views.book_pass, name='book_pass'),
    path('book/<int:workshift_id>/', views.book_pass, name='book_pass'),
]
