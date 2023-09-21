from django.urls import path

from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
     path('account/login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name = 'account-login'),
    path('account/dashboard/', views.index, name = 'account-dashboard'),
]