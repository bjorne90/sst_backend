from django.urls import path
from . import views
from booking.views import book_pass

app_name = 'scheduling'

urlpatterns = [
    path('list/', views.workshift_list, name='workshift_list'),
    path('book/', views.book_workshift, name='book_workshift'),
    path('book/<int:workshift_id>/', views.book_workshift, name='book_workshift'),
    path('book-pass/<int:workshift_id>/', book_pass, name='book_pass'),
    path('work-shifts/', views.work_shifts, name='work_shifts'),
    path('work-shifts/add-event/', views.add_event, name='add_event'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar2/', views.calendar_view, name='calendar2'),
    path('employees_calendar/', views.employees_calendar_view, name='employees_calendar'),
    path('cancel/<int:workshift_id>/', views.cancel_workshift, name='cancel_workshift'),
]
