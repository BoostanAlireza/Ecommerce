from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from uuid import uuid4

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    def __str__(self):
        return self.title

class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{str(self.discount)} | {self.description}'

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discounts = models.ManyToManyField(Discount, blank=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images')

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS_CHOICES = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS_CHOICES, default=COMMENT_STATUS_WAITING)

    objects = models.Manager()
    approved = ApprovedCommentManager()


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    datetime_created = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField()

    unique_together = ['cart', 'product']


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_CANCELED, 'Canceled')
    ] 
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
                    max_length=1,
                    choices=ORDER_STATUS_CHOICES, 
                    default=ORDER_STATUS_UNPAID
                    )
    
    def __str__(self):
        return f'Order id {self.id}'
    

    def get_total_price(self):
        return sum(item.quantity * item.unit_price for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    unique_together = ['order', 'product']


class Address(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    