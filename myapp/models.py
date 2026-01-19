from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

class Product(models.Model):
    # --- Mandatory Fields ---
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    # --- Optional Fields ---
    # blank=True allows the field to be empty in forms.
    # null=True allows the database to store a NULL value.
    product_model = models.CharField(max_length=100, blank=True, null=True)
    available_size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., S, M, L, XL or 10, 11, 12")
    color = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0, blank=True, null=True)

    # --- Boolean Tick Fields ---
    # default=False means they are unchecked by default.
    is_featured = models.BooleanField(default=False, verbose_name="Featured Product")
    is_on_sale = models.BooleanField(default=False, verbose_name="Price Off Product")
    
    # --- Auto-managed Fields ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order products by name by default when you query them
        ordering = ['name']

    def __str__(self):
        return self.name