from rest_framework import status
import pytest
from model_bakery import baker
from store.models import Collection
from rest_framework.test import APIClient

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        #AAA
        #Arrange
        #Act
        response = create_collection({'name': 'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  

    def test_if_user_is_not_admin_returns_403(self, force_authentication, create_collection):
        #AAA
        #Arrange
        force_authentication(is_staff=False)
        #Act
        response = create_collection({'name': 'a'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN  
               
    def test_if_data_is_invalid_returns_400(self, force_authentication, create_collection):
        #AAA
        #Arrange
        force_authentication(is_staff=True)
        #Act
        response = create_collection({'name': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None
        
    def test_if_data_is_valid_returns_201(self, force_authentication, create_collection):
        #AAA
        #Arrange
        force_authentication(is_staff=True)
        #Act
        response = create_collection({'name': 'a'})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
 
 
@pytest.mark.django_db        
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self):
        
        collection = baker.make(Collection)
        
        api_client = APIClient()
        response = api_client.get(f"/store/collections/{collection.id}/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'name': collection.name,
            'products_count': 0
        }
        
    def test_if_collection_not_exists_return_404(self):
        
        collection_id = 0
        
        api_client = APIClient()
        response = api_client.get(f"/store/collections/{collection_id}/")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND