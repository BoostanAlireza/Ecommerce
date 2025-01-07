from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'inventory', 'category_title']
    list_select_related = ['category']
    list_editable = ['unit_price']
    list_filter = ['category']
    list_per_page = 10
    prepopulated_fields = {
        'slug': ['title']
    }

    @admin.display(ordering='category__title')
    def category_title(self, product):
        return product.category.title
    
admin.site.register(models.Category)


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 0
    min_num = 1

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'datetime_created']
    inlines = [OrderItemInline]


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    def first_name(self, customer):
        return customer.user.first_name

    def last_name(self, customer):
        return customer.user.last_name

    def email(self, customer):
        return customer.user.email