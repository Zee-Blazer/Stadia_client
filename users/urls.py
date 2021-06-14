from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="users/files/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
    path('forgot_password/', auth_views.PasswordResetView.as_view(template_name="users/forgot_password.html"),
         name="forgot_password"),
    # path('change_password/', auth_views.PasswordChangeView.as_view(template_name="users/change_password.html"),
    #      name="change_password"),
]
