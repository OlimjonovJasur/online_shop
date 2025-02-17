from django.urls import path, include
from shop import views

app_name = 'shop'


urlpatterns = [
    path('', views.IndexView.as_view(), name='products'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category-detail/<int:category_id>/', views.IndexView.as_view(), name='products_of_category'),
    path('order-detail/<int:pk>/save/', views.OrderDetailView.as_view(), name = 'order_detail'),
    path('create-product/', views.ProductCreateView.as_view(), name='product_create'),
    path('delete-product/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('edit-product/<int:pk>/', views.ProductEditView.as_view(), name='product_edit'),
    path('product-comments/<int:pk>/', views.CommentView.as_view(), name='comment_view'),
]
