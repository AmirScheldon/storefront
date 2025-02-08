from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.HelloViewSet.as_view())
]
