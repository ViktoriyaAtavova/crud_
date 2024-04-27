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
            stock_product = StockProduct(
                product=position['product'],
                quantity=position['quantity'],
                price=position['price'],
                stock=stock
            )
            stock_product.save()

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')
        
        stock = super().update(instance, validated_data)

        for position in positions:
            instance = StockProduct(
                product=position['product'],
                quantity=position['quantity'],
                price=position['price'],
                stock=stock
            )
            instance.save()

        return stock
