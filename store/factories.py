import random
import factory
from faker import Faker
from factory.django import DjangoModelFactory
from . import models


faker = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.Category

    title = factory.Faker(
        'sentence',
        nb_words=5,
        variable_nb_words=True
    )
    description = factory.Faker(
        'paragraph', nb_sentences=1, variable_nb_sentences=False)


class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = models.Discount

    discount = factory.LazyFunction(lambda: random.randint(1, 50)/100)
    description = factory.Faker(
        'paragraph', nb_sentences=1, variable_nb_sentences=False)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    title = factory.LazyAttribute(lambda x: ' '.join(
        [x.capitalize() for x in faker.words(3)]))
    slug = factory.LazyAttribute(lambda x: '-'.join(x.title.split(' ')).lower())
    unit_price = factory.LazyFunction(
        lambda: random.randint(1, 1000) + random.randint(0, 100)/100)
    inventory = factory.LazyFunction(lambda: random.randint(1, 1000))
    description = factory.Faker(
        'paragraph', nb_sentences=1, variable_nb_sentences=True)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = models.Comment

    name = factory.Faker('first_name')
    body = factory.Faker('paragraph', nb_sentences=4,
                            variable_nb_sentences=True)
    status = factory.LazyFunction(
        lambda: random.choice(
            ([models.Comment.COMMENT_STATUS_APPROVED,
                models.Comment.COMMENT_STATUS_WAITING,
                models.Comment.COMMENT_STATUS_NOT_APPROVED])
        )
    )


# class AddressFactory(DjangoModelFactory):
#     class Meta:
#         model = models.Address

#         province = factory.Faker('province')
#         city = factory.Faker('city')
#         street = factory.LazyFunction(lambda: f'street {factory.Factory('word')} {
#                                       random.randint(1, 100)}')
