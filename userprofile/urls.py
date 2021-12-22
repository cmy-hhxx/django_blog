from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='userprofile'

urlpatterns = [
        path('login/', views.user_login, name='login'),
        path('logout/', views.user_logout, name='logout'),
        path('register/', views.user_register, name='register'),
        path('delete/<int:id>/', views.user_delete, name='delete'),
        #path('reset_password/', auth_views.PasswordResetView.as_view()),
        #path('reset_password_done/', auth_views.PasswordResetDoneView.as_view()),
]
