from django.urls import path
from .views import (
    WorkShiftListCreateView, 
    BookWorkShiftView, 
    CancelWorkShiftView,
    WorkShiftDetailView,
    ListAllWorkShiftsView  # Import the new view
)

app_name = 'scheduling'

urlpatterns = [
    path('list/', WorkShiftListCreateView.as_view(), name='workshift_list'),
    path('list/<int:pk>/', WorkShiftDetailView.as_view(), name='workshift_detail'),
    path('all/', ListAllWorkShiftsView.as_view(), name='all_workshifts'),  # Add this line
    path('book/', BookWorkShiftView.as_view(), name='book_workshift_list'),
    path('book/<int:workshift_id>/', BookWorkShiftView.as_view(), name='book_specific_workshift'),
    path('cancel/<int:workshift_id>/', CancelWorkShiftView.as_view(), name='cancel_workshift'),
]
