from django.urls import path
from . import views
from rest_framework_nested import routers
# router generate URL pattern for ViewSets for us.

"""
    DefaultRouter:
        * it shows us API ROOT at store ENDPOINT
        * it shows us json file by using product.json
"""
router = routers.DefaultRouter()
router.register('products', views.ProductViewSets, basename= 'products')
router.register('collections', views.CollectionViewSets)

review_router = routers.NestedSimpleRouter(router, 'products', lookup= 'products')
review_router.register('reviews', views.ReviewsViewSets, basename= 'products-reviews')

urlpatterns = router.urls + review_router.urls