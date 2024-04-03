from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "content_type", "created")
    raw_id_fields = ("user",)
    readonly_fields = ("transaction_id",)

    # list_filter = (
    #     "status",
    #     ("created", DateRangeFilter),
    #     AutocompleteFilterFactory("Пользователь", "user"),
    # )
