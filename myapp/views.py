from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product

# --- HOME PAGE VIEW ---
def home(request):
    # Fetch all featured products
    featured_product_list = Product.objects.filter(is_featured=True).order_by('name')
    flash_products = Product.objects.filter(is_on_sale=True)

    # Pagination: 12 products per page
    paginator = Paginator(featured_product_list, 12)
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # All categories for home page category section
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'flash_products': flash_products,
    }
    return render(request, 'index.html', context)


# --- PRODUCTS PAGE VIEW ---
def product_list(request):
    product_queryset = Product.objects.all()
    
    paginator = Paginator(product_queryset, 12)
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products}
    return render(request, 'products.html', context)


# --- CATEGORY LIST PAGE VIEW ---
def category_list(request):
    category_queryset = Category.objects.all()
    paginator = Paginator(category_queryset, 16)  # 16 categories per page
    page_number = request.GET.get('page')

    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'categories': categories})


# --- CATEGORY DETAIL PAGE VIEW ---
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product_list = Product.objects.filter(category=category).order_by('name')

    # Pagination: 12 products per page
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category_detail.html', context)

    