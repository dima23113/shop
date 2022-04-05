from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Product, ProductSize, ImgProduct


class ImgSerializer(ModelSerializer):
    class Meta:
        model = ImgProduct
        fields = ['img']


class SizeSerializer(ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['name', 'qty']


class ProductSerializer(ModelSerializer):
    product_sizer = SizeSerializer(many=True)
    product_img = ImgSerializer(many=True)
    category = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    subcategory = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    subcategory_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    brand = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = Product
        fields = ['category', 'subcategory', 'subcategory_type', 'brand', 'name', 'slug', 'description',
                  'specifications', 'price', 'available', 'price_discount', 'product_sizer', 'product_img']
