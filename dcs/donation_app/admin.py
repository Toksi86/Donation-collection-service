from django.contrib import admin

from .models import Payment, Collect


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'reason', 'planned_amount', 'end_date')
    exclude = ('collected_amount', 'contributors_count')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'amount', 'collect')
    exclude = ('timestamp', 'contributors_count')
