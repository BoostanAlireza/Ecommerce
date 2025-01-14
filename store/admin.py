from django.contrib import admin
from django.urls import reverse
from django.db.models import Count
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from . import models



class CustomInventoryFilter(admin.SimpleListFilter):
    LESS_THAN_5 = '<5'
    BETWEEN_5_AND_10 = '5<=10'
    MORE_THAN_10 = '>10'
    title = 'Inventory Status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return[
            (CustomInventoryFilter.LESS_THAN_5, 'Shortage'),
            (CustomInventoryFilter.BETWEEN_5_AND_10, 'OK'),
            (CustomInventoryFilter.MORE_THAN_10, 'No Shoratge')
        ]

    def queryset(self, request, queryset):
        if self.value() == CustomInventoryFilter.LESS_THAN_5:
            return queryset.filter(inventory__lt=5)
        if self.value() == CustomInventoryFilter.BETWEEN_5_AND_10:
            return queryset.filter(inventory__range=(5, 10))
        if self.value() == CustomInventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price',
                    'inventory', 'inventory_status', 'category_title', 'number_of_comments']
    list_select_related = ['category']
    list_editable = ['unit_price']
    list_filter = ['category', CustomInventoryFilter]
    list_per_page = 10
    search_fields = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }

    @admin.display(ordering='category__title')
    def category_title(self, product):
        return product.category.title
    

    def get_queryset(self, request):
        return super().get_queryset(request) \
                .prefetch_related('comments') \
                .annotate(comments_count=Count('comments'))
    
    @admin.display(description='# comments', ordering='comments_count')
    def number_of_comments(self, product):
        url = (
            reverse('admin:store_comment_changelist')
            + '?'
            + urlencode({
                'product__id': product.id
            })

        )
        return format_html('<a href="{}">{}</a>', url, product.comments_count)
    
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Critical'
        if product.inventory > 100:
            return 'Abundance'
        return 'Medium'
    
admin.site.register(models.Category)


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 0
    min_num = 1

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status',
                    'datetime_created', 'number_of_items']
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('items') \
            .annotate(
                items_count=Count('items')
            )

    @admin.display(description='# items', ordering='items_count')
    def number_of_items(self, order):
        return order.items_count
    

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
    

class CartItemInline(admin.TabularInline):
    model = models.CartItem
    fields = ['id', 'product', 'quantity']
    extra = 0
    min_num = 1

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'datetime_created']
    inlines = [CartItemInline]

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'datetime_created', 'status']
    list_select_related = ['product']
    list_editable = ['status']
    autocomplete_fields = ['product']
    list_per_page = 10