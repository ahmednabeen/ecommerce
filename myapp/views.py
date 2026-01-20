# yourproject/yourapp/views.py

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product


# --- VIEW FOR THE HOME PAGE (NOW WITH FEATURED PRODUCTS & PAGINATION) ---
def home(request):
    # Fetch all products marked as featured
    featured_product_list = Product.objects.filter(is_featured=True).order_by('name')
    
    # Set up the Paginator: 12 products per page
    paginator = Paginator(featured_product_list, 12)
    page_number = request.GET.get('page') # Get page number from URL (e.g., /?page=2)

    try:
        # Get the Page object for the requested page number
        paginated_featured_products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_featured_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_featured_products = paginator.page(paginator.num_pages)

    # You can still pass other context like categories if you need them on the home page
    all_categories = Category.objects.all()

    context = {
        'products': paginated_featured_products, # Pass the paginated products to the template
        'categories': all_categories,
    }
    return render(request, 'index.html', context)


# --- VIEW FOR THE PRODUCTS PAGE (WITH PAGINATION) ---
def product_list(request):
    product_queryset = Product.objects.all()
    
    paginator = Paginator(product_queryset, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {'products': products}
    return render(request, 'products.html', context)

