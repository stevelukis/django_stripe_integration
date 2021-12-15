from django.contrib import admin

from orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'paid', 'timestamp']


admin.site.register(Order, OrderAdmin)
