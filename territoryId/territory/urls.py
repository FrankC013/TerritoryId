from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('sign_up/', views.register, name='sign_up'),
    path('login/login_success/', views.success, name='login_success'),
    path('face_register/', views.face_register, name='face_register'),
]
