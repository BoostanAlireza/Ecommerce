
from rest_framework import serializers
from .models import Customer, Product, Category



class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.SerializerMethodField()
    
    def get_num_of_products(self, category):
        return category.products.count()
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'num_of_products']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'inventory', 'category', 'description']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'birth_date']

    



