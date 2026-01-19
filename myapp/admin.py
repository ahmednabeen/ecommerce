from django.contrib import admin
from .models import Category, Product  # Import the new Product model

# --- Class to customize how Products are displayed in the admin ---
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured', 'is_on_sale')
    list_filter = ('category', 'is_featured', 'is_on_sale')
    search_fields = ('name', 'description', 'product_model')
    list_editable = ('price', 'stock', 'is_featured', 'is_on_sale')

# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin) # Register Product with its custom admin class
