from . import views
from django.urls import path


app_name = 'user_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
