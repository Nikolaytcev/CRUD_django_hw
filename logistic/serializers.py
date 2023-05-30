from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):

        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')
        positions_list = list(instance.positions.all())
        stock = super().update(instance, validated_data)

        for position in positions:
            pos = positions_list.pop(0)
            pos.product = position.get('product', pos.product)
            pos.quantity = position.get('quantity', pos.quantity)
            pos.price = position.get('price', pos.price)
            pos.save()

        return stock
