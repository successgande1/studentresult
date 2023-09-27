from django.contrib import admin
from .models import Profile, SubscriptionPlan, Subscription, BusinessAccount, SubscriptionHistory


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'full_name', 'phone', 'address', 'description')
    list_per_page = 6


admin.site.register(Profile, ProfileAdmin)


admin.site.register(SubscriptionPlan)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan', 'pin', 'expiration_date', 'duration_days')
    list_per_page = 6


admin.site.register(Subscription, SubscriptionAdmin)

admin.site.register(BusinessAccount)

admin.site.register(SubscriptionHistory)
