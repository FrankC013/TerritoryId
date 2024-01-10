from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('sign_up/', views.register, name='sign_up'),
    path('login_success/', views.success, name='login_success'),
    path('face_register/', views.face_register, name='face_register'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
