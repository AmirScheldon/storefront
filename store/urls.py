from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list),
    #<int:id>: use Converter to avoid responsing to non-integer 
    path('product/<int:id>/', views.product_detail),
    path('collection/<int:pk>/', views.collection_detail, name= 'colllection_detail')
]
