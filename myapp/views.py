from django.shortcuts import render
from .models import Category


# Make your views here.

def home(request):
    # Fetch all Category objects from the database
    categories = Category.objects.all()
    
    # Pass the categories to the template in the context dictionary
    context = {
        'categories': categories
    }
    return render(request, 'index.html', context)
