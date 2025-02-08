from django.urls import path
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products', views.ProductViewSets, basename= 'products')
router.register('collections', views.CollectionViewSets)
router.register('carts', views.CartViewSets )
router.register('customer', views.CustomerViewSets)
router.register('order', views.OrderViewSets, basename= 'order')

review_router = routers.NestedSimpleRouter(router, 'products', lookup= 'products')
review_router.register('reviews', views.ReviewsViewSets, basename= 'products-reviews')

image_router= routers.NestedSimpleRouter(router, 'products', lookup = 'products')
image_router.register('images', views.ProductImageViewSets, basename= 'products-images')

items_router = routers.NestedSimpleRouter(router, 'carts', lookup= 'carts')
items_router.register('items', views.CartItemViewSets, basename= 'carts-items')

urlpatterns = router.urls + review_router.urls + items_router.urls + image_router.urls