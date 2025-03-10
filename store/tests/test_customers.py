import pytest
from django.contrib.auth.models import User
from rest_framework import status
from store.models import Customer


@pytest.fixture
def list_customers(api_client):
    def do_list_customers():
        return api_client.get(f'/store/customers/')
    return do_list_customers

@pytest.mark.django_db
class TestRetrieveCustomer:
    def test_if_user_is_not_admin_returns_403(self, authenticate, list_customers):
        authenticate(is_staff=False)

        response = list_customers()

        assert response.status_code == status.HTTP_403_FORBIDDEN
