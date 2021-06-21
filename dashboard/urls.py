from . import views
from django.urls import path


app_name = 'user_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('programs/', views.programs, name='programs'),
    path('all_events/', views.all_events, name='all_events'),
    path('create_event/', views.create_event, name='create_event'),
    path('ticket/<int:ticket_id>/', views.view_ticket, name="ticket"),
    path('created_events/', views.created_events, name='created_events'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('attend_event/<str:event_name>/', views.add_event, name="add_event"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]
