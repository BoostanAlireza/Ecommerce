import pytest
from django.contrib.auth.models import User
from rest_framework import status
from store.models import Product, Category, ProductImage
from model_bakery import baker

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

@pytest.mark.django_db
class TestCreationProduct:
    def test_if_user_is_ananymous_returns_401(self, create_product):
        response = create_product({'title': 'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_401(self, authenticate, create_product):
        authenticate(is_staff=False)

        response = create_product({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)

        category = baker.make(Category)

        product = {
            'title': 'a',
            'unit_price': 10.99,
            'inventory': 100,
            'category': category.id,
            'description': 'This is some dummy data'
        }
        response = create_product(product)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self, api_client):
        product = baker.make(Product)
        response = api_client.get(f'/store/products/{product.id}/')
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': product.id,
            'title': product.title,
            'unit_price': product.unit_price,
            'inventory': product.inventory,
            'description': product.description,
            'category': product.category.id,
            'images': []
        }
