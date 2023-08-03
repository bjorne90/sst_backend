from django.urls import path
from .views import (
    WorkShiftListCreateView, 
    BookWorkShiftView, 
    CancelWorkShiftView
)
from booking.views import book_pass

app_name = 'scheduling'

urlpatterns = [
    path('list/', WorkShiftListCreateView.as_view(), name='workshift_list'),
    path('book/', BookWorkShiftView.as_view(), name='book_workshift'),
    path('book/<int:workshift_id>/', BookWorkShiftView.as_view(), name='book_workshift'),
    path('book-pass/<int:workshift_id>/', book_pass, name='book_pass'),
    path('cancel/<int:workshift_id>/', CancelWorkShiftView.as_view(), name='cancel_workshift'),
]
