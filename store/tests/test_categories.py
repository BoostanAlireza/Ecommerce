import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreationCategory:
    # @pytest.mark.skip
    def test_if_user_is_ananymous_returns_401(self):
        # Arrange

        # Act
        client = APIClient()
        response = client.post('/store/categories/', { 'title': 'a' })

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post('/store/categories/', { 'title': 'a' })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/categories/', { 'title': '' })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
    def test_if_data_is_valid_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/categories/', { 'title': 'a' })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
