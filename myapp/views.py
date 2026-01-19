from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Category, Product


# --- VIEW FOR THE HOME PAGE ---
def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'index.html', context)


# --- VIEW FOR THE PRODUCTS PAGE (WITH PAGINATION) ---
def product_list(request):
    product_queryset = Product.objects.all()
    
    paginator = Paginator(product_queryset, 12)  # ✅ 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {'products': products}
    return render(request, 'products.html', context)
