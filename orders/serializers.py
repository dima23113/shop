from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    product = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'qty', 'size', 'price_discount']


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    total_discount_cost = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'payment_status', 'customer', 'status', 'payment_id', 'items',
                  'total_cost', 'total_discount_cost']

    def get_total_discount_cost(self, obj):
        return obj.total_discount_cost()

    def get_total_cost(self, obj):
        return obj.total_cost()
