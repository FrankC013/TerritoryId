from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
]
