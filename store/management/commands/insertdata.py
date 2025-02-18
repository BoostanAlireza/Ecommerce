import random
import factory
from faker import Faker
from datetime import datetime, timedelta
from django.utils import timezone

from django.db import transaction
from django.core.management.base import BaseCommand
from store.models import Category, Product, Discount, Comment
from store.factories import (
    CategoryFactory,
    ProductFactory,
    DiscountFactory,
    CommentFactory,
)


faker = Faker()

list_of_models = [Category, Product, Discount, Comment]

NUMBER_OF_CATEGORIES = 10
NUMBER_OF_DISCOUNTS = 100
NUMBER_OF_PROUDUCTS = 1000
NUMBER_OF_ADRRESSES = 130

class Command(BaseCommand):
    help = 'This class generates dummy data'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Deleting old data. Please be patient.')

        for model in list_of_models:
            model.objects.all().delete()

        self.stdout.write('Generating new data...')
        
        timezone_info = timezone.get_current_timezone()

        #Generating data for gategories table
        categories = [CategoryFactory(featured_product=None) for _ in range(NUMBER_OF_CATEGORIES)]
        print(f'Successfully created {NUMBER_OF_CATEGORIES} categories.')

        # Generating data for discounts table
        discounts = [DiscountFactory() for _ in range(NUMBER_OF_DISCOUNTS)]
        print(f'Successfully created {NUMBER_OF_DISCOUNTS} discounts.')

        # Generating data for products table
        products = []
        for _ in range(NUMBER_OF_PROUDUCTS):
            product = ProductFactory(category_id=random.choice(categories).id)
            product.datetime_created = datetime(random.randint(2000, 2024), random.randint(1, 12), random.randint(1, 15), tzinfo=timezone.now().tzinfo)
            product.datetime_modified = product.datetime_created + timedelta(days=random.randint(1, 100))
            product.save()
            products.append(product)
        print(f'Successfully created {NUMBER_OF_PROUDUCTS} products.')

        # Generating data for comments table
        for product in products:
            for _ in range(random.randint(1, 20)):
                comment = CommentFactory(product_id=product.id)
                comment.datetime_created = datetime(
                                    random.randint(2000, 2024),
                                    random.randint(1, 12), 
                                    random.randint(1, 15), 
                                    tzinfo=timezone.now().tzinfo)
                comment.save()
        print(f'Successfully created comments.')




