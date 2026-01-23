from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST


# --- HOME PAGE VIEW ---
def home(request):
    featured_product_list = Product.objects.filter(is_featured=True).order_by('name')
    flash_products = Product.objects.filter(is_on_sale=True)
    paginator = Paginator(featured_product_list, 12)
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

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
    paginator = Paginator(category_queryset, 16)  
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

# --- Product Detail PAGE VIEW ---

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)

# --- ABOUT,contact, privacy, terms_of_service PAGE VIEW ---

def about(request):
    return render(request, 'about.html')    
def contact_page(request):
    return render(request, 'contact.html')
def privacy_policy_page(request):
    return render(request, 'privacy_policy.html')
def terms_of_service_page(request):
    return render(request, 'terms_of_service.html')

# ------------- CART PAGE VIEW ---------------

def add_to_cart(request, product_id ):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    product_id_str = str(product_id)
    
    quantity = int(request.POST.get('quantity', 1))

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    else:
        cart[product_id_str] = {'quantity': quantity, 'price': str(product.price)} 
    request.session['cart'] = cart
    
    return JsonResponse({'status': 'success', 'message': 'Item added to cart'})

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    cart_items = []
    total_price = 0

    # This part of your logic is correct
    for product_id, item in cart.items():
        # Make sure you have a Product model imported
        product = get_object_or_404(Product, id=int(product_id)) 
        item_total = product.price * item['quantity']
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'item_total': item_total,
        })
        total_price += item_total

    # Define the context dictionary
    context = {
    'cart_items': cart_items,
    'total_price': total_price,
    'shipping_fee': 495,
    'grand_total': total_price + 495,
    'cart_count': cart_count,
    }
    return render(request, 'cart_detail.html', context)

@require_POST # Ensures this view only accepts POST requests
def update_cart(request):
    try:
        # Load the JSON data sent from the frontend
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        new_quantity = int(data.get('quantity'))

        cart = request.session.get('cart', {})

        if product_id in cart:
            if new_quantity > 0:
                cart[product_id]['quantity'] = new_quantity
                request.session['cart'] = cart
                # You can recalculate totals here and send them back if you want
                return JsonResponse({'status': 'success', 'message': 'Cart updated.'})
            else:
                # If quantity is 0 or less, remove the item (optional)
                del cart[product_id]
                request.session['cart'] = cart
                return JsonResponse({'status': 'success', 'message': 'Item removed.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Product not in cart.'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))

        cart = request.session.get('cart', {})

        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
def remove_selected_from_cart(request):
        try:
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])

            cart = request.session.get('cart', {})

            for pid in product_ids:
                pid = str(pid)
                if pid in cart:
                    del cart[pid]

            request.session['cart'] = cart
            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

