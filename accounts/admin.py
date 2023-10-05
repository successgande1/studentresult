from django.contrib import admin
from .models import Profile, SubscriptionPlan, Subscription, BusinessAccount, SubscriptionHistory


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'full_name', 'phone', 'address')
    list_per_page = 6


admin.site.register(Profile, ProfileAdmin)


admin.site.register(SubscriptionPlan)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan', 'pin', 'expiration_date', 'duration_days')
    list_per_page = 6


admin.site.register(Subscription, SubscriptionAdmin)


class BusinessAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'address', 'lga', 'state', 'subscription_plan', 'is_active', 'created_date')
    list_per_page = 6


admin.site.register(BusinessAccount, BusinessAccountAdmin)


class SubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display = ('business_account', 'plan', 'pin', 'start_date', 'expiration_date')
    list_per_page = 6


admin.site.register(SubscriptionHistory, SubscriptionHistoryAdmin)
