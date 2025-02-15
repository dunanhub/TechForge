from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {'categories': categories})

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products/products_by_category.html', {'category': category, 'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer