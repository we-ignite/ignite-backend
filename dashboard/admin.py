from django.contrib import admin
from dashboard.models import Events,Entries,Payment

# Register your models here.

admin.site.register(Events)
admin.site.register(Entries)
admin.site.register(Payment)
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('entry', 'payment_id', 'order_id', 'signature')
#     search_fields = ('entry__team_name', 'payment_id', 'order_id')