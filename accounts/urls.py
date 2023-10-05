from django.urls import path

from . import views
from .views import (
    SubscriptionPlanListView,
    SubscriptionPlanDetailView,
    SubscriptionPlanCreateView,
    SubscriptionPlanUpdateView,
    SubscriptionPlanDeleteView, SubscriptionListView,
    SubscriptionDeleteView, SubscriptionDetailView
)
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('account/login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='account-login'),
    path('account/dashboard/', views.index, name='account-dashboard'),
    path('subscription-plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    path('subscription-plans/<int:pk>/', SubscriptionPlanDetailView.as_view(), name='subscription-plan-detail'),
    path('subscription-plans/create/', SubscriptionPlanCreateView.as_view(), name='subscription-plan-create'),
    path('subscription/plans/<int:pk>/update/', SubscriptionPlanUpdateView.as_view(), name='subscription-plan-update'),
    path('subscription-plans/<int:pk>/delete/', SubscriptionPlanDeleteView.as_view(), name='subscription-plan-delete'),
    path('create/subscription/', views.generate_subscription, name='create-subscription'),
    path('subscription/list/', SubscriptionListView.as_view(), name='subscription-list'),
    path('subscription/detail/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='delete-subscription'),
    path('create/business/account/', views.create_business_account, name='create_business_account'),
    path('activate/business/account/<int:business_account_id>/subscription/', views.pin_activation, name='activate_business_account'),
    path('create/admin/account/<int:business_account_id>/', views.create_admin_user, name='create_admin_business_user'),
    path('create/teacher/account/', views.create_teacher_user, name='create_teacher_user'),
    path('create/management/staff/', views.create_management_staff, name='account-create-management-staff'),
    path('staff/list/', views.staff_list, name='account-staff-list'),
    path('staff/profile/update/', views.user_profile_update, name='account_profile_update'),
    path('staff/profile/', views.user_profile, name='account_profile'),
    path('disable_user/<int:pk>/', views.disable_user, name='account-disable-user'),
    path('enable_user/<int:pk>/', views.enable_user, name='account-enable-user'),
    path('change-password/', views.change_password, name='account-change-password'),
    path('change-password/', views.change_password, name='account-change-password'),
    path('password-change-done/', views.password_change_done, name='account-password-change-done'),
    path('logout/', auth_view.LogoutView.as_view(template_name='accounts/logout.html'), name='account-logout'),
]
