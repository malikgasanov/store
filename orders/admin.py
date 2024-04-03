from django.contrib import admin

from orders.models import Order, OrderPosition


class OrderPositionInline(admin.StackedInline):
    model = OrderPosition
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')
    inlines = (OrderPositionInline,)
