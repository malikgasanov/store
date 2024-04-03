from rest_framework import serializers

from products.models import Product, Category


class SubcategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField(method_name='get_name', required=False)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name


class CategorySerializer(serializers.ModelSerializer):
    childs = SubcategorySerializer(many=True, partial=True, source='parents', required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'childs',
        ]

    def get_childs(self, obj):
        return obj.parents.values('id', 'name')

    def _get_child_ids(self, childs):
        return (data['id'] for data in childs if 'id' in data)

    def _create_subcategory(self, childs, instance):
        categories = (
            Category(name=data['name'], parent=instance)
            for data in childs if 'id' not in data and 'name' in data
        )
        Category.objects.bulk_create(categories)

    def create(self, validated_data):
        if 'parents' in validated_data:
            childs = validated_data.pop('parents')
            child_ids = self._get_child_ids(childs)
            instance = super().create(validated_data)
            self._create_subcategory(childs, instance)
            for category in Category.objects.filter(pk__in=child_ids):
                category.parent = instance
                category.save()
            return instance
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'parents' in validated_data:
            childs = validated_data.pop('parents')
            child_ids = self._get_child_ids(childs)
            self._create_subcategory(childs, instance)
            for category in Category.objects.filter(pk__in=child_ids):
                category.parent = instance
                category.save()
        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'discount_price',
            'stock_quantity',
            'product_features'
        ]
