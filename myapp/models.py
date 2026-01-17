from django.db import models

# Create your models here.

from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # 'slug' is a URL-friendly version of the name, e.g., "home-kitchen"
    slug = models.SlugField(max_length=100, unique=True)
    # 'upload_to' specifies the subdirectory in your media folder
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        # Correctly pluralizes 'Category' to 'Categories' in the admin panel
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # This generates the URL for a specific category page
        return reverse('category_detail', args=[self.slug])
