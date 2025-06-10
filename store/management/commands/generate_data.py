from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
import random
from store.factories import CategoryFactory, ProductFactory, DiscountFactory, CommentFactory
from store.models import Category, Product, Discount, Comment


class Command(BaseCommand):
    help = 'Generates sample data for the store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=10,
            help='Number of categories to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=1000,
            help='Total number of products to create'
        )
        parser.add_argument(
            '--discounts',
            type=int,
            default=100,
            help='Number of discounts to create'
        )
        parser.add_argument(
            '--comments-per-product',
            type=int,
            default=20,
            help='Maximum number of comments per product'
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Delete existing data
                self.stdout.write('Deleting old data...')
                for model in [Category, Product, Discount, Comment]:
                    model.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(
                    'Old data deleted successfully'))

                # Create categories
                self.stdout.write('Creating categories...')
                categories = CategoryFactory.create_batch(
                    options['categories'],
                    featured_product=None
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Created {len(categories)} categories'))

                # Create discounts
                self.stdout.write('Creating discounts...')
                discounts = DiscountFactory.create_batch(options['discounts'])
                self.stdout.write(self.style.SUCCESS(
                    f'Created {len(discounts)} discounts'))

                # Create products
                self.stdout.write('Creating products...')
                products = []
                for _ in range(options['products']):
                    product = ProductFactory(
                        category=random.choice(categories))
                    # Set random creation and modification dates
                    product.datetime_created = datetime(
                        random.randint(2000, 2024),
                        random.randint(1, 12),
                        random.randint(1, 15),
                        tzinfo=timezone.now().tzinfo
                    )
                    product.datetime_modified = product.datetime_created + timedelta(
                        days=random.randint(1, 100)
                    )
                    product.save()
                    products.append(product)
                self.stdout.write(self.style.SUCCESS(
                    f'Created {len(products)} products'))

                # Assign random discounts to products
                for product in products:
                    num_discounts = random.randint(0, 2)
                    if num_discounts > 0:
                        product_discounts = random.sample(
                            discounts, num_discounts)
                        product.discounts.add(*product_discounts)

                # Create comments for products
                self.stdout.write('Creating comments...')
                for product in products:
                    num_comments = random.randint(
                        1, options['comments_per_product'])
                    for _ in range(num_comments):
                        comment = CommentFactory(
                            product=product,
                            status=Comment.COMMENT_STATUS_APPROVED
                        )
                        comment.datetime_created = datetime(
                            random.randint(2000, 2024),
                            random.randint(1, 12),
                            random.randint(1, 15),
                            tzinfo=timezone.now().tzinfo
                        )
                        comment.save()
                self.stdout.write(self.style.SUCCESS(
                    'Created comments for products'))

                self.stdout.write(self.style.SUCCESS(
                    'Successfully generated all sample data'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error generating data: {str(e)}'))
            raise
