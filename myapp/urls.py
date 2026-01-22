from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Home Page
    path('products/', views.product_list, name='product_list'),  # All Products Page 
    path('categories/', views.category_list, name='category_list'), # Category pages 
    path('category/<slug:slug>/', views.category_detail, name='category_detail'), # Category_Detail pages 
    path('about/', views.about, name='about'), # About Page 
    path('contact/', views.contact_page, name='contact'), # Contact Page 
    path('privacy-policy/', views.privacy_policy_page, name='privacy_policy'), # privacy-policy page
    path('terms-of-service/', views.terms_of_service_page, name='terms_of_service'), #terms-of-service page
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  #product_detail
    path('cart/', views.view_cart, name='view_cart'), # Cart page
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Cart Page
    path('cart/update/', views.update_cart, name='update_cart'), # Cart Page
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'), # delete button active in cart 
]