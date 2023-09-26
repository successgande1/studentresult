from django.urls import path

from . import views
from .views import (
    SubscriptionPlanListView,
    SubscriptionPlanDetailView,
    SubscriptionPlanCreateView,
    SubscriptionPlanUpdateView,
    SubscriptionPlanDeleteView, VoucherListView
)
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('account/login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='account-login'),
    path('account/dashboard/', views.index, name='account-dashboard'),
    path('subscription-plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    path('subscription-plans/<int:pk>/', SubscriptionPlanDetailView.as_view(), name='subscription-plan-detail'),
    path('subscription-plans/create/', SubscriptionPlanCreateView.as_view(), name='subscription-plan-create'),
    path('subscription-plans/<int:pk>/update/', SubscriptionPlanUpdateView.as_view(), name='subscription-plan-update'),
    path('subscription-plans/<int:pk>/delete/', SubscriptionPlanDeleteView.as_view(), name='subscription-plan-delete'),
    path('create/voucher/', views.generate_voucher, name='create-voucher'),
    path('list-voucher/', VoucherListView.as_view(), name='voucher-list'),
    path('create/management/staff/', views.create_management_staff, name='account-create-management-staff'),
    path('staff/list/', views.staff_list, name='account-staff-list'),
    path('staff/profile/', views.user_profile, name='account-profile'),
    path('disable_user/<int:pk>/', views.disable_user, name='account-disable-user'),
    path('enable_user/<int:pk>/', views.enable_user, name='account-enable-user'),
    path('change-password/', views.change_password, name='account-change-password'),
    path('change-password/', views.change_password, name='account-change-password'),
    path('password-change-done/', views.password_change_done, name='account-password-change-done'),
    path('logout/', auth_view.LogoutView.as_view(template_name='accounts/logout.html'), name='account-logout'),
]
