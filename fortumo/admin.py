from django.contrib import admin

from .models import (
    Message,
    Payment,
    Service,
)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'message', 'sender', 'shortcode')
admin.site.register(Message, MessageAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('service', 'message', 'pin', 'used')
admin.site.register(Payment, PaymentAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_id', 'ips', 'validate_ip')
admin.site.register(Service, ServiceAdmin)
