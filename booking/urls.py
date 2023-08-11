from django.urls import path
from . import views
from rest_framework import routers

app_name = 'booking'

router = routers.DefaultRouter()
router.register(r'booking', views.BookingViewSet)

urlpatterns = [
    path('list/', views.booking_list, name='booking_list'),
    path('book/', views.book_pass, name='book_pass'),
    path('book/<int:workshift_id>/', views.book_pass, name='book_pass'),
    path('api/booked-list/', views.api_booking_list, name='api_booking_list'),
]
