from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.reg_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('test/', views.test, name='test'),
    path('change_password/', views.change_password, name='pass_changer'),
]
