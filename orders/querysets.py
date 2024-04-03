from django.db.models import QuerySet, Sum, F, IntegerField


class OrderQuerySet(QuerySet):
    def with_amount_and_count(self):
        return self.aggregate(
            price=Sum(
                F('orderposition__product__price'),
                default=0,
                output_field=IntegerField()
            ),
            discount_price=Sum(
                F('orderposition__product__discount_price'),
                default=0,
                output_field=IntegerField()
            ),
            count=Sum('orderposition__quantity')
        )
