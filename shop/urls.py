from django.urls import path, include

from shop import views

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('order-detail/<int:pk>/save/', views.order_detail, name = 'order_detail')
]
