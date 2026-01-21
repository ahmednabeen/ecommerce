from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Home Page
    path('products/', views.product_list, name='product_list'),  # All Products Page 
    path('categories/', views.category_list, name='category_list'), # Category pages 
    path('category/<slug:slug>/', views.category_detail, name='category_detail'), # Category_Detail pages 
    path('about/', views.about, name='about'), # About Page 
]