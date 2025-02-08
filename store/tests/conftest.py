import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def force_authentication(api_client):
    def do_force_authentication(is_staff=True):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_force_authentication