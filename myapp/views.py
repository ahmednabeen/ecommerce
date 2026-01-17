from django.shortcuts import render


# Make your views here.

def index(request):
    return render(request, 'index.html')
