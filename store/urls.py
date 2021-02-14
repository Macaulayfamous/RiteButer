from django.urls import path
from .import views
from .views import ProductDetailView


urlpatterns = [
    path('', views.home,name='home'),
    path('cart_detail/', views.cart_detail,name='cart_detail'),
    path('card/add/<product_id>', views.add_cart,name='add_cart'),
    path('<slug:category_slug>/', views.home,name='products_by_category'),

    path('post/<int:pk>/',ProductDetailView.as_view(),name='product-detail'),
    
]