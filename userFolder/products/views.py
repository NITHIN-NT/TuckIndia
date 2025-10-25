from django.shortcuts import render
from .models import Product,ProductImage,Category
from django.utils import timezone
from datetime import date

# Create your views here.
def homepage(request):
    products = Product.objects.select_related('category').order_by('?')[:4]
    featured_products = Product.objects.filter(is_featured=True).order_by('?')[:4]
    most_demanded = Product.objects.filter(is_most_demanded=True).order_by('?')[:4]
    today = timezone.now().date()
    new_arrivals = Product.objects.filter(created_at__date=today).order_by('?')[:4]
    context = {
        'products' : products,
        'featured_products' : featured_products,
        'most_demanded' : most_demanded,
        'new_arrivals' : new_arrivals
    }
    return render(request,'products/home.html',context)


 