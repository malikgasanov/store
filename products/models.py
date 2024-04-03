from django.db import models


class Category(models.Model):
    name = models.CharField('название', max_length=256)
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True, related_name='parents')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=256)
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.00)
    discount_price = models.DecimalField('цена со скидкой', max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField('количество на складе', default=0)
    product_features = models.JSONField('характеристики товара')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
