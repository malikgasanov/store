from django.contrib import admin

from carts.models import Cart, CartProduct


class CartProductInline(admin.StackedInline):
    model = CartProduct
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = (CartProductInline,)
